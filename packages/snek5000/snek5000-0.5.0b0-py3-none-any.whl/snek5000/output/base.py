"""Manage user case files.

"""
import inspect
import os
import pkgutil
import shutil
from itertools import chain
from pathlib import Path
from socket import gethostname

from fluidsim_core.output import OutputCore
from inflection import underscore
from snek5000 import __version__, get_asset, logger, mpi, resources


class Output(OutputCore):
    """Container and methods for getting paths of and copying case files.

    A path object :code:`self.root` points to the directory containing the
    case files.

    """

    @property
    def excludes(self):
        """Prefixes and suffixes of files which should be excluded from being
        copied."""
        return {"prefix": "__", "suffix": (".vimrc", ".tar.gz", ".o", ".py")}

    @property
    def makefile_usr_sources(self):
        """
        Sources for inclusion to makefile_usr.inc
        Dict[directory]  -> list of source files
        """
        return {
            # "source_directory": [
            #    (src1a.f, src1b.f)
            #    (src2a.f, src2b.f, src2c.f), ...
            # ]
        }

    @property
    def makefile_usr_obj(self):
        """Object files to be included in compilation. Should be exported as USR
        environment variable.

        """
        makefile_usr_obj = [
            sources[0].replace(".f", ".o")
            for sources in chain.from_iterable(self.makefile_usr_sources.values())
        ]
        return makefile_usr_obj

    @staticmethod
    def _complete_info_solver(info_solver):
        """Complete the ParamContainer info_solver."""
        OutputCore._complete_info_solver(info_solver)

        classes = info_solver.classes.Output.classes
        classes._set_attrib(
            "PrintStdOut",
            dict(
                module_name="snek5000.output.print_stdout",
                class_name="PrintStdOut",
            ),
        )
        classes._set_attrib(
            "PhysFields",
            dict(module_name="snek5000.output.phys_fields", class_name="PhysFields"),
        )

    @staticmethod
    def _complete_params_with_default(params, info_solver):
        """This static method is used to complete the *params* container."""
        # Bare minimum
        attribs = {
            "ONLINE_PLOT_OK": True,
            "period_refresh_plots": 1,
            "HAS_TO_SAVE": True,
            "sub_directory": "",
        }
        params._set_child("output", attribs=attribs)

    @classmethod
    def get_root(cls):
        """Get the path to the current package."""
        # Better than

        # root = Path(__file__).parent?

        #  with resources.path(__name__, "__init__.py") as f:
        #      root = f.parent

        root = Path(inspect.getmodule(cls).__file__).parent
        return root

    @classmethod
    def get_configfile(cls, host=None):
        """Get path of the Snakemake configuration file for the current machine.
        All configuration files are stored under ``etc`` sub-package.

        """
        if not host:
            host = os.getenv(
                "SNIC_RESOURCE", os.getenv("GITHUB_WORKFLOW", gethostname())
            )
        root = cls.get_root()
        configfile = root / "etc" / f"{host}.yml"

        if not configfile.exists():
            logger.warning(
                "Expected a configuration file describing compilers and flags: "
                f"{configfile}"
            )
            configfile = Path(get_asset("default_configfile.yml"))
            logger.info(f"Using default configuration instead: {configfile}")

        return configfile

    def __init__(self, sim=None):
        self.sim = sim
        try:
            self.name_solver = sim.info.solver.short_name
        except AttributeError:
            pass

        self.root = self.get_root()
        # Check configfile early
        self.get_configfile()

        if sim:
            self.oper = sim.oper

            # Same as package name __name__
            super().__init__(sim)

            dict_classes = sim.info.solver.classes.Output.import_classes()

            # initialize objects
            for cls_name, Class in dict_classes.items():
                # only initialize if Class is not the Simul class
                if not isinstance(self, Class):
                    setattr(self, underscore(cls_name), Class(self))

    def _init_sim_repr_maker(self):
        """Adds mesh description to name of the simulation. Called by the
        ``_init_name_run`` method"""
        sim_repr_maker = super()._init_sim_repr_maker()
        self.oper._modify_sim_repr_maker(sim_repr_maker)

        return sim_repr_maker

    def _get_resources(self, name_solver=None):
        """Get a generator of resources (files) in a package, excluding
        directories (subpackages).

        :returns: generator

        """
        excludes = self.excludes
        if not name_solver:
            name_solver = self.name_solver
        try:
            contents_pkg = resources.contents(name_solver)
        except TypeError:
            return ()
        except ImportError:
            raise FileNotFoundError(
                f"Cannot resolve subpackage name_solver={name_solver} at root={self.root}"
            )

        return (
            f
            for f in contents_pkg
            if (
                resources.is_resource(name_solver, f)
                and not any(f.startswith(ext) for ext in excludes["prefix"])
                and not any(f.endswith(ext) for ext in excludes["suffix"])
            )
        )

    def _get_subpackages(self):
        """Get a dictionary of subpackages with values generated by
        :func:`get_resources`.

        :returns: dict

        """
        root = self.root
        name_solver = self.name_solver
        subpackages = {
            subpkg.name.replace(f"{root.name}.", ""): self._get_resources(subpkg.name)
            for subpkg in pkgutil.walk_packages([str(root)], prefix=f"{name_solver}.")
        }

        return subpackages

    def get_paths(self):
        """Get a list of paths to all case files.

        :returns: list

        """
        paths = []

        # abl.usr -> /path/to/abl/abl.usr
        paths += [self.root / resource for resource in self._get_resources()]

        for subpkg, res in self._get_subpackages().items():
            # toolbox -> /path/to/abl/toolbox
            subpkg_root = self.root / subpkg.replace(".", os.sep)
            # main.f -> /path/to/abl/toolbox/main.f
            paths += [subpkg_root / resource for resource in res]
        return paths

    def copy(self, new_dir, force=False):
        """Copy case files to a new directory. The directory does not have to be present.

        :param new_dir: A str or Path-like instance pointing to the new directory.
        :param force: Force copy would overwrite if files already exist.

        """
        # Avoid race conditions! Should be only executed by rank 0.
        if mpi.rank != 0:
            return

        abs_paths = self.get_paths()
        subpackages = self._get_subpackages()

        root = self.root

        def conditional_ignore(src, names):
            """Ignore if not found in ``abs_paths``."""
            src = Path(src)
            include = abs_paths + [root / subpkg for subpkg in subpackages]
            exclude = tuple(
                name
                for name in names
                if not any((src / name) == path for path in include)
            )

            logger.debug(
                "".join(
                    (
                        f"- src: {src}",
                        "\n- include:\n",
                        "\n ".join(str(name) for name in include),
                        "\n- exclude:\n",
                        "\n ".join(exclude),
                        "\n----",
                    )
                )
            )
            return exclude

        new_root = Path(new_dir)
        try:
            logger.info("Copying with shutil.copytree ...")
            copytree_kwargs = dict(
                src=root, dst=new_root, symlinks=False, ignore=conditional_ignore
            )
            # Python 3.8+
            shutil.copytree(**copytree_kwargs, dirs_exist_ok=True)
        except (TypeError, shutil.Error):
            try:
                logger.warning(
                    "Python < 3.8: shutil.copytree may not proceed if "
                    "directories exist."
                )
                # Hoping that new_root has not been created
                shutil.copytree(**copytree_kwargs)
            except FileExistsError as e:
                logger.warning(e)
                logger.info("Copying with shutil.copy2 ...")
                # Copy one by one from the scratch
                if not new_root.exists():
                    logger.debug(f"Creating {new_root} ...")
                    os.makedirs(new_root, exist_ok=True)

                for abs_path in abs_paths:
                    rel_path = abs_path.relative_to(root)
                    new_path = new_root / rel_path
                    if not new_path.parent.exists():
                        os.makedirs(new_path.parent)

                    logger.debug(f"Copying {new_path}")
                    if new_path.exists():
                        if force:
                            logger.warning(f"{new_path} would be overwritten ...")
                        else:
                            logger.warning(
                                f"{new_path} exists, skipping. Use force=True to overwrite."
                            )
                            continue

                    shutil.copy2(abs_path, new_path)
        finally:
            logger.info(f"Copied: {root} -> {new_root}")

    def write_box(self, template):
        """Write <case name>.box file from box.j2 template."""
        if mpi.rank == 0:
            box_file = self.sim.path_run / f"{self.name_solver}.box"
            logger.info(f"Writing box file... {box_file}")
            with open(box_file, "w") as fp:
                self.sim.oper.write_box(
                    template, fp, comments=self.sim.params.short_name_type_run
                )

    def write_size(self, template):
        """Write SIZE file from SIZE.j2 template."""
        if mpi.rank == 0:
            size_file = self.sim.path_run / "SIZE"
            logger.info(f"Writing SIZE file... {size_file}")
            with open(size_file, "w") as fp:
                self.oper.write_size(
                    template, fp, comments=self.sim.params.short_name_type_run
                )

    def write_makefile_usr(self, template):
        """Write the makefile_usr.inc file which gets included in the main
        makefile.

        """

        paths_of_sources = []

        for path_dir, list_of_sources in self.makefile_usr_sources.items():
            for sources in list_of_sources:
                paths_of_sources.append([f"{path_dir}/{file}" for file in sources])

        if mpi.rank == 0 and paths_of_sources:
            makefile_usr = self.sim.path_run / "makefile_usr.inc"
            output = template.render(
                list_of_sources=paths_of_sources,
                comments=self.sim.params.short_name_type_run,
            )
            with open(makefile_usr, "w") as fp:
                fp.write(output)

    def post_init(self):
        if mpi.rank == 0:
            _banner_length = 42
            logger.info("*" * _banner_length)
            logger.info(f"solver: {self.__class__}")
            logger.info(f"path_run: {self.path_run}")
            logger.info("*" * _banner_length)

        # This also calls _save_info_solver_params_xml
        super().post_init()

        # Write source files to compile the simulation
        if mpi.rank == 0 and self._has_to_save and self.sim.params.NEW_DIR_RESULTS:
            self.copy(self.path_run)

    def _save_info_solver_params_xml(self, replace=False):
        """Saves the par file, along with FluidSim's params_simul.xml and info.xml"""
        params = self.sim.params
        if mpi.rank == 0 and self._has_to_save and params.NEW_DIR_RESULTS:
            par_file = Path(self.path_run) / f"{self.name_solver}.par"
            logger.info(
                f"Writing params files... {par_file}, params_simul.xml, "
                "info_solver.xml"
            )
            with open(par_file, "w") as fp:
                params.nek._write_par(fp)

        super()._save_info_solver_params_xml(replace, comment=f"snek5000 {__version__}")
