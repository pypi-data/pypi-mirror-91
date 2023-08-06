from __future__ import annotations

import abc
from dataclasses import dataclass
from enum import Enum
import functools
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Collection, Dict, List, Optional, Union

from packaging.specifiers import SpecifierSet
from pipreqs import pipreqs
import pkg_resources
from pkg_resources import Requirement
import yaml

# https://www.python.org/dev/peps/pep-0610/
PACKAGE_URL_METAFILE = "direct_url.json"


def execute_conda_command(args: List[str]) -> str:
    process = subprocess.run(["conda"] + args,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             universal_newlines=True,
                             check=False)
    output = process.stdout.strip() + process.stderr.strip()
    return output


class RuleLabels(Enum):
    PIP_NAME_MAPPING = "pip_name_mapping"
    CONDA_NAME_MAPPING = "conda_name_mapping"
    SYSTEM = "system"


@dataclass
class PrintableWarning:
    package_name: str
    message: str

    def __str__(self):
        return f"{self.package_name}: {self.message}"


@functools.lru_cache(maxsize=None)
def _get_rule_maps() -> Dict[str, Dict[str, str]]:
    """
    Parsing the rule files for mapping python package names, conda names
    and finding out the system dependencies. The whole rule set is built by
    keeping the parsed pypi name as reference. The parsed pypi name is the
    name of a package as listed in pypi but replaced all the hyphens with
    underscores. Below given are few examples of parsed pypi name

            Import name : sklearn
            Parsed pypi : scikit_learn
            pypi name   : scikit-learn

    For more details, refer the documentation in the YAML rule file
    """
    rule_file = Path(__file__).parent / "dependency_rules/dependency_rules.yml"
    mappings = yaml.safe_load(rule_file.open())
    mandatory_keys = {val.value for val in RuleLabels}
    # Both must have exactly the same elements
    if mandatory_keys.symmetric_difference(mappings.keys()):
        raise RuntimeError("Rule file is corrupted")
    out = {}
    for k in mandatory_keys:
        out[k] = dict(mapping.strip().split(":") for mapping in mappings[k])

    # nested parsing of system dependencies
    for name, value in out[RuleLabels.SYSTEM.value].items():
        out[RuleLabels.SYSTEM.value][name] = value.split(",")

    return out


def _get_system_deps(name: str) -> List[str]:
    """
    Get the list of system dependencies required for a python package. For
    example graphviz is required to have graphviz and xdg-utils installed
    in the system apart from the python package itself.

    Parameters
    ----------
    name:
        Parsed pypi name

    Returns
    -------
    List of system dependencies required for a python package to be working
    """
    system_rules = _get_rule_maps()[RuleLabels.SYSTEM.value]
    return system_rules.get(name, [])


def _conda2parsed_pypi(name: str) -> str:
    """
    Parsed pypi names are being used as the standard for making comparisons
    in this module. For instance, conda list the package pytorch as
    "pytorch" while pip list it as "torch". This function converts conda name
    ("pytorch" to parsed pypi name ("torch") using the predefined mapping rule
    """
    conda_rules = _get_rule_maps()[RuleLabels.CONDA_NAME_MAPPING.value]
    return conda_rules.get(name, name).replace("-", "_")


def _source2parsed_pypi(name: str) -> str:
    """
    Parsed pypi names are being used as the standard for making comparisons
    in this module. This function converts the `import` name to the parsed
    pypi name. While both names are same for almost all the cases, there are
    few that isn't. For example sklearn is the import name while scikit-learn
    is the pypi name (and scikit_learn is the parsed pypi name - note the
    underscore). Note that for python's dependency manager, both "-" and "_"
    has same meaning. scikit-learn = scikit_learn
    """
    pypi_rules = _get_rule_maps()[RuleLabels.PIP_NAME_MAPPING.value]
    return pypi_rules.get(name, name).replace("-", "_")


@dataclass
class BasePackage:
    """Base Package class for holding the PIP and Conda Spec.

    Custom Package classes must be inherited from this class to include
    custom logic for equality check and parsing
    """
    name: str

    def __eq__(self, other: BasePackage) -> bool:
        raise NotImplementedError


@dataclass
class CondaPackage(BasePackage):
    """
    Do not call the constructor / init directly. Use classmethod(s) instead
    """
    version: Optional[str] = None
    build: Optional[str] = None

    def __post_init__(self):
        self.parsed_name = _conda2parsed_pypi(self.name)

    @classmethod
    def from_string(cls, string):
        try:
            name, version, build = string.split("=")
        except ValueError:
            raise RuntimeError("Error while parsing the dependency spec from "
                               "yaml file. Raise the issue with Grid support")
        if not all((name, version, build)):
            raise ValueError("Arguments cannot be undefined for conda spec")
        return cls(name=name, version=version, build=build)

    def __str__(self):
        return f"{self.name}={self.version}={self.build}"

    def __eq__(self, other: CondaPackage):
        if other.__class__ is self.__class__:
            return all(
                (self.build == other.build, self.version == other.version,
                 self.parsed_name == other.parsed_name))
        return NotImplemented


@dataclass
class PipPackage(BasePackage):
    """
    Offload all parsing, de-parsing, checks etc to `Requirement` object.
    Do not call the constructor / init directly. Use classmethod(s) instead
    """
    def __post_init__(self):
        # This is assigned here only for documentation purpose. The value
        # will actually populated in `from_requirement` method
        self.parsed_name = self.name.replace("-", "_")
        self.requirement_obj: Optional[Requirement] = None

    @classmethod
    def from_string(cls, string):
        # Not catching parsing error
        # pkg_resources.extern.packaging.requirements.InvalidRequirement
        # This will be raised for the requirements installed with
        # `python setup.py develop`. However `pip install -e .` doesn't
        # have this issue
        req = Requirement.parse(string)
        return cls.from_requirement(req)

    @classmethod
    def from_requirement(cls, req):
        self = cls(req.project_name)
        self.requirement_obj = req
        return self

    def _version_check(self, other: PipPackage):
        """
        Checking the versions of two instances with special constraints.

        This fine grained check is triggered only in the case basic
        equality check (==) fails. It is for making sure version inclusion
        checks will pass. Specifically, version for package info fetched from
        environment would always has `==` as the version specifier since
        exact version is known. But version specifier for packages from
        requirements.txt could be any (`>` or `>=` or ...)

        Constraints:
            1. Number of specifier to the `self` must be 1. This is to
                make sure next constraint is valid
            2. The only specifier exist on `self` is `==`. This is to
                make sure the `self` knows exact version
            3. The version of `self` is included in the version of `other`
                Eg: `"pkg==1.2.0" == pkg>1.0.0,<=2.0.0

        Note: This check is based on the strong assumption that `other` is
        also a `PipPackage` but not a `CondaPackage`
        """
        if len(self.requirement_obj.specifier) > 1:
            # expecting other.__eq__ to solve the equality check
            return NotImplemented
        specifier = tuple(self.requirement_obj.specifier)[0]
        if specifier.operator != "==":
            # expecting other.__eq__ to solve the equality check
            return NotImplemented
        # checking at-least one specifier on the other side has
        # non-empty version
        for sp in other.requirement_obj.specifier:
            if sp.version:
                break
        else:
            return False
        # TODO: check for prereleases
        return specifier.version in other.requirement_obj.specifier

    def __str__(self):
        return str(self.requirement_obj)

    def __eq__(self, other: PipPackage):
        if self.__class__ != other.__class__:
            return NotImplemented
        if self.requirement_obj == other.requirement_obj:
            return True
        return self._version_check(other)


class DependencyManagerBase(abc.ABC):
    """Dependency manager base class.

    The dependency managers such as pip or conda or any future managers
    such as poetry should subclassed from this base class. The Abstract
    methods are specific to each package manager and should be implemented
    by the child class. These methods are being called in the setup time
    to build the information base by parsing the dependency listing and
    analyzing the environment file. It's also being utilized to write
    the dependency listing back to the package manager specific file
    """
    def __init__(self):
        self._setup()

    @abc.abstractmethod
    def write_spec(self):
        """Write the dependency spec after formatting based on the dependency manager.
        """
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def _get_default_req_file() -> Path:
        """Get the Path object for the requirement file for each dependency manager.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _read_file_deps(self) -> Dict[str, BasePackage]:
        """Implement reading the requirement listing for each package manager.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _fetch_env_deps(self) -> Dict[str, BasePackage]:
        """Implement reading dependencies from current environment.
        """
        raise NotImplementedError

    def _setup(self):
        self._warnings: List[PrintableWarning] = []
        self._source_deps_list: List[str] = self._scan_source_deps()

        # Reading package manager specific methods to build information base
        self.req_file: Path = self._get_default_req_file()
        self.file_deps: Dict[str, BasePackage] = self._read_file_deps()
        self.env_deps: Dict[str, BasePackage] = {}
        for k, v in self._fetch_env_deps().items():
            if k in self._source_deps_list:
                self.env_deps[k] = v

    @property
    def has_change(self):
        """
        Return True if any change is needed. False other wise.
        """
        if not self.req_file.exists():
            return True
        if set(self._source_deps_list) - set(self.file_deps):
            return True
        for key in self._source_deps_list:
            if key not in self.env_deps:
                continue
            if self.env_deps[key] != self.file_deps[key]:
                return True

    @property
    def warnings(self) -> str:
        warnings = "\n".join((str(w) for w in self._warnings))
        return warnings

    @staticmethod
    def _scan_source_deps() -> List[str]:
        # TODO: This could take a lot of time if files are a lot (1000s)
        """Scan source code in the CWD (recursively) and finds the
        package dependencies

        This information will then be used as the reference while fetching
        information from different sources such as current environment,
        requirement listing, pypi etc
        """
        ignore_dirs = [
            "venv", "test", "tests", "_test", "_tests", "egg", "EGG", "info",
            "docs", "__pycache__"
        ]
        input_path = Path.cwd()
        for pth in input_path.iterdir():
            # ignore directories beginning with ('.' and '__')
            if pth.is_dir() and (pth.name.startswith('.')
                                 or pth.name.startswith('__')):
                ignore_dirs.append(pth.name)

        # TODO: remove pipreqs dependency
        # other considerations: pydeps & pigar
        candidates = pipreqs.get_all_imports(input_path,
                                             encoding=None,
                                             extra_ignore_dirs=ignore_dirs,
                                             follow_links=True)
        return [_source2parsed_pypi(c) for c in candidates]

    def get_missing(self) -> Collection[str]:
        """
        Get packages with proper information is missing. Any package which
        is found installed in environment and found specified in the
        requirement listing file (even if no version is specified), will
        be considered as "not missing". Other packages present in the source
        code will be returned as "missing"
        """
        available = set(self.env_deps) | set(self.file_deps)
        return set(self._source_deps_list) - available

    def collate_final(self):
        """
        Collate the final list of requirements for writing back to the
        disk.

        It loops through all the existing requirements in the requirement
        listing file and make sure the the spec (eg: version) hasn't been
        changed by comparing with the spec of installed package. It then
        loops through the packages those are missing in the requirement
        listing and add the spec by fetching it from the environment
        """
        if self.get_missing():
            raise ValueError("Found requirements without spec identified")
        collated = []
        # don't union on env_deps since it could have non-necessary packages.
        # That might be true for file_deps as well but that's something user
        # gave us explicitly and hence ignoring. Also, valid_names must keep
        # the order of values in requirements file
        missing = set(self._source_deps_list) - set(self.file_deps)
        valid_names = list(self.file_deps.keys()) + sorted(list(missing))
        for name in valid_names:
            if name in self.env_deps and name in self.file_deps:
                if self.env_deps[name] == self.file_deps[name]:
                    # Preferring file deps in case both are equal to avoid
                    # losing other information such as markers
                    collated.append(self.file_deps[name])
                else:
                    collated.append(self.env_deps[name])
            elif name in self.file_deps:
                collated.append(self.file_deps[name])
            elif name in self.env_deps:
                collated.append(self.env_deps[name])
        return collated

    def write_config(self, config: Dict):
        names = set()
        for n in self._source_deps_list:
            names |= set(_get_system_deps(n))
        if names:
            # TODO: config file path is hardcoded
            config_file = Path("config.yml")
            config_file.touch(exist_ok=True)
            # Sorting to make the order deterministic
            sys_deps_action = f"apt install -y {' '.join(sorted(names))}"
            if "actions" not in config["compute"]:
                config["compute"]["actions"] = {"on_image_build": []}
            elif "on_image_build" not in config["compute"]["actions"]:
                config["compute"]["actions"]["on_image_build"] = []

            if not isinstance(config["compute"]["actions"]["on_image_build"],
                              list):
                raise RuntimeError("Parsing error while reading config.yml")

            config["compute"]["actions"]["on_image_build"].append(
                sys_deps_action)
            yaml.safe_dump(config, config_file.open(mode="w+"))


class CondaManager(DependencyManagerBase):
    _env_name: Optional[str] = None
    _prefix: Optional[str] = None
    _channels: List[str] = []

    @staticmethod
    def _build_dependency_dict(
            specs: List) -> Dict[str, Union[CondaPackage, PipPackage]]:
        """
        Build dependency objects from the spec

        Parameters
        ----------
        specs:
            Dependency specs read from the environment.yml file. It would
            contain the all the dependencies formatted as "name=version=build".
            It would also contain PIP dependencies as a dictionary with
            key as "pip". An example `specs` is given below

            specs = ["numpy-base=1.19.2=py38hcfb5961_0",
                     "ninja=1.10.2=py38hf7b0b51_0",
                     ...
                     {"pip": ["absl-py==0.11.0"
                              "attrs==20.2.0",
                              ...
                             ]
                     }
                     ]

            We are not expecting it to contain a dictionary with key other than
            "pip" and hence we throw if that's the case

        Returns
        -------
        A dictionary that maps the parsed pypi name of each dependency to the
        Package object. Since conda dependency listing has both conda and
        pip spec, the return value would contain both CondaPackage and
        PipPackage containers
        """
        dependencies = {}
        pip_dependencies = []
        for d in specs:
            if isinstance(d, dict):
                if "pip" not in d or len(d) > 1:
                    raise RuntimeError("Could not parse the conda yaml file. "
                                       "Raise the issue with Grid support")
                pip_dependencies = d["pip"]
            else:
                dep = CondaPackage.from_string(d)
                dependencies[dep.parsed_name] = dep
        for elem in pip_dependencies:
            dep = PipPackage.from_string(elem)
            dependencies[dep.parsed_name] = dep
        return dependencies

    def _read_file_deps(self) -> Dict[str, CondaPackage]:
        """
        Read environment.yml to fetch user defined dependencies
        """
        if self.req_file.exists():
            specs = yaml.safe_load(self.req_file.read_text())
            if not isinstance(specs, dict):
                raise RuntimeError(f"Parsing error with {self.req_file}")
            self._env_name = specs.get("name")
            self._prefix = specs.get("prefix")
            self._channels = self._channels + specs["channels"]
            return self._build_dependency_dict(specs["dependencies"])
        return {}

    @staticmethod
    def _get_default_req_file() -> Path:
        return Path("environment.yml")

    def _fetch_env_deps(self) -> Dict[str, CondaPackage]:
        """
        Fetch dependencies from currently active conda environment
        """
        if not os.getenv("CONDA_DEFAULT_ENV"):
            return {}
        export = execute_conda_command(["env", "export"])
        specs = yaml.safe_load(export)

        self._env_name = self._env_name or specs.get("name")
        self._channels = self._channels + specs["channels"]
        return self._build_dependency_dict(specs["dependencies"])

    def write_spec(self):
        """
        Write requirements to `environment.yml`
        """
        final = {}
        if self._env_name:
            final["name"] = self._env_name
        if self._prefix:
            final["prefix"] = self._prefix
        final["channels"] = sorted(list(set(self._channels)))
        conda_deps = []
        pip_deps = []
        collated = self.collate_final()
        for dep in collated:
            if isinstance(dep, PipPackage):
                pip_deps.append(str(dep))
            else:
                conda_deps.append(str(dep))
        final["dependencies"] = conda_deps
        final["dependencies"].append({"pip": pip_deps})  # noqa
        yaml.safe_dump(final, self.req_file.open(mode="w+"))


class PipManager(DependencyManagerBase):
    def _read_file_deps(self) -> Dict[str, PipPackage]:
        """
        Read requirements.txt to fetch user defined dependencies
        """
        file_deps = {}
        if self.req_file.exists():
            # Not catching parsing error
            # pkg_resources.extern.packaging.requirements.InvalidRequirement
            # This will be raised for the requirements installed with
            # `python setup.py develop`. However `pip install -e .` doesn't
            # have this issue
            for req in pkg_resources.parse_requirements(
                    self.req_file.read_text()):
                dep = PipPackage.from_requirement(req)
                file_deps[dep.parsed_name] = dep
        return file_deps

    @staticmethod
    def _get_default_req_file() -> Path:
        return Path("requirements.txt")

    def _fetch_env_deps(self) -> Dict[str, PipPackage]:
        """
        Look at the currently active environment to fetch the list of installed
        dependencies.
        """
        out = {}
        working_set = pkg_resources.working_set
        if working_set is None:
            return out
        # identifying dependencies of dependencies but not using that to
        # to make more filtering at this phase
        sub_reqs = {}
        for ws in working_set:  # skipcq: PYL-E1133
            for req in ws.requires():
                dep = PipPackage.from_requirement(req)
                sub_reqs[req.project_name] = dep
            if self._is_dist_editable(ws):
                warn = PrintableWarning(ws.project_name,
                                        'Package is installed as "editable"')
                self._warnings.append(warn)
            req = ws.as_requirement()
            url = self._get_distribution_url(ws)
            if url:
                req.url = self._get_distribution_url(ws)
                req.specifier = SpecifierSet("")
            # TODO: identify hashCmp, marker when possible
            dep = PipPackage.from_requirement(req)
            out[dep.parsed_name] = dep
        return out

    def write_spec(self):
        """
        Write requirements to `requirements.txt`
        """
        collated = self.collate_final()
        out = "\n".join((str(val) for val in collated))
        Path("requirements.txt").write_text(out)

    @staticmethod
    def _get_distribution_url(
            dist: pkg_resources.Distribution) -> Optional[str]:
        """
        Fetch the distribution URL from package distribution based on pep440
        and pep610. Different details about how this feature eventually landed
        in `pip` and different considerations can be found at the issue page -
        https://github.com/pypa/pip/issues/609.
        """
        try:
            url_meta = json.loads(dist.get_metadata(PACKAGE_URL_METAFILE))
        except (FileNotFoundError, ValueError, UnicodeDecodeError):
            return None
        url = url_meta.get("url")
        if not url:
            return None
        if "vcs_info" in url_meta:
            commit_id = url_meta["vcs_info"].get("commit_id")
            vcs = url_meta["vcs_info"].get("vcs")
            return f"{vcs}+{url}@{commit_id}"
        return url

    @staticmethod
    def _is_dist_editable(dist: pkg_resources.Distribution) -> bool:
        """
        Check if a Distribution is installed as editable
        """
        for path_item in sys.path:
            egg_link = Path(path_item) / dist.project_name / '.egg-link'
            if egg_link.is_file():
                return True
        return False
