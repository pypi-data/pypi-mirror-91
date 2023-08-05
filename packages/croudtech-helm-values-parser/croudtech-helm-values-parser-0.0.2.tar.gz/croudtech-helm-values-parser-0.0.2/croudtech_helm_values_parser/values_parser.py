import copy
import json
import os
from glob import glob
import yaml


class ValuesParser:
    non_environment_directories = [
        "reckoner_files",
        "manifests",
        "environments",
        "kube",
        "kube-system",
        "backups",
    ]
    non_app_filenames = [
        "common.yaml",
        "system.yaml",
    ]

    def __init__(self, repo, output_format, output_indent=2):
        self.repo = os.path.abspath(repo)
        self.output_format = output_format
        self.output_indent = output_indent

    @property
    def release_list(self):
        if not hasattr(self, "_release_list"):
            self._release_list = ReleaseList(repo=self.repo)
        return self._release_list

    def get_release_properties(self, key, environments=[], namespaces=[], charts=[]):
        values = self.release_list.get_release_properties(
            key=key,
            environments=list(environments),
            namespaces=list(namespaces),
            charts=list(charts),
        )
        if self.output_format == "json":
            return json.dumps(values, indent=self.output_indent)

    def build_all_values_files(
        self,
        destination,
        environments=None,
        namespaces=None,
        charts=None,
        output_type="yaml",
    ):
        combined_data = self.release_list.build_all_values_files(
            destination=destination,
            environments=list(environments),
            namespaces=list(namespaces),
            charts=list(charts),
            output_type=output_type,
        )
        destination_directory = os.path.abspath(destination)
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)
        for destination_file, data in combined_data:
            destination_path = os.path.join(destination_directory, destination_file)
            stream = open(destination_path, "w")
            print(destination_path)
            if output_type == "yaml":
                data_string = yaml.dump(data, stream, Dumper=yaml.Dumper)
            elif output_type == "json":
                json.dump(data, stream, indent=2, default=str)


class ReleaseList:
    def __init__(self, repo):
        self.repo = repo

    def get_release_properties(
        self, key, environments=None, namespaces=None, charts=None
    ):
        releases = self.releases(
            environments=environments, namespaces=namespaces, charts=charts
        )
        return sorted(list(set([getattr(release, key) for release in releases])))

    def build_all_values_files(
        self,
        destination,
        environments=None,
        namespaces=None,
        charts=None,
        output_type="yaml",
    ):
        for release in self.releases(
            environments=environments, namespaces=namespaces, charts=charts
        ):
            destination_file = "%s.%s" % (release.release, output_type)
            data = release.combined_values
            yield (destination_file, data)

    def releases(self, environments=None, namespaces=None, charts=None):
        if not hasattr(self, "_releases"):
            self._releases = list()
            for file in self.list_files():
                release = Release(base_path=self.repo, path=file)
                if release.is_release:
                    self._releases.append(release)
        if environments is not None and len(environments) > 0:
            return self.filter_releases("environment", environments)
        elif namespaces is not None and len(namespaces) > 0:
            return self.filter_releases("namespace", namespaces)
        elif charts is not None and len(charts) > 0:
            return self.filter_releases("chart", charts)
        return self._releases

    def filter_releases(self, key, values):
        if values is not None and len(values) > 0:
            if type(values) != list:
                values = [values]
            filtered_releases = []
            for release in self._releases:
                if getattr(release, key) in values:
                    filtered_releases.append(release)
            return filtered_releases
        return []

    def list_files(self):
        leaves = []
        for root, dirs, files in os.walk(self.repo):
            if not dirs:
                for file in files:
                    if file[-5:] == ".yaml":
                        leaves.append(os.path.join(root, file))

        return leaves


class Release:
    def __init__(self, base_path, path):
        self.base_path = base_path
        self.path = path

    dict_attributes = [
        "path",
        "base_path",
        "parts",
        "app_name",
        "is_release",
        "chart",
        "release",
        "environment",
        "all_files",
    ]

    ignore_folders = [
        "reckoner_files",
        "backups",
        "environments",
        "manifests",
    ]

    def as_dict(self):
        return {item: getattr(self, item) for item in self.dict_attributes}

    @property
    def parts(self):
        if not hasattr(self, "_parts"):
            self._parts = self.path.replace(self.base_path, "").split("/")[1:]
        return self._parts

    @property
    def is_release(self):
        if self.app_name in ["common", "system"]:
            return False
        for item in self.parts:
            if item[0] in [".", "_"]:
                return False
        for part in self.parts:
            if part in self.ignore_folders:
                return False
        return True

    @property
    def app_name(self):
        return self.parts[-1].replace(".yaml", "")

    @property
    def chart(self):
        if not hasattr(self, "_chart"):
            self._chart = self.parts[-2]
        return self._chart

    @property
    def release(self):
        if not hasattr(self, "_release"):
            self._release = "-".join(self.parts).replace(".yaml", "")

        return self._release

    @property
    def environment(self):
        if not hasattr(self, "_environment"):
            self._environment = self.parts[0]

        return self._environment

    @property
    def namespace(self):
        if not hasattr(self, "_namespace"):
            self._namespace = "-".join(self.parts[0:-2])

        return self._namespace

    @property
    def files(self):
        if not hasattr(self, "_files"):
            self._files = []
            for filepath in self.all_files:
                if os.path.exists(filepath):
                    self._files.append(filepath)
        return self._files

    @property
    def all_files(self):
        files = list()
        parts = copy.deepcopy(self.parts)
        while len(parts) > 0:
            parts.pop()
            path = os.path.join(self.base_path, *parts, "common.yaml")
            files.append(path)
            path = os.path.join(self.base_path, *parts, "_system.yaml")
            files.append(path)

        files = sorted(files, key=files.index, reverse=True)
        files.append(self.path)

        files.insert(
            3,
            os.path.join(
                self.base_path,
                self.environment,
                self.parts[1],
                "_%s" % self.chart,
                "common.yaml",
            ),
        )
        files.insert(
            4,
            os.path.join(
                self.base_path,
                self.environment,
                self.parts[1],
                "_%s" % self.chart,
                "_system.yaml",
            ),
        )

        return files

    @property
    def values(self):
        if not hasattr(self, "_values"):
            self._values = dict()
            for file in self.files:
                self._values[file] = yaml.load(
                    open(file, mode="r", encoding="UTF-8"), Loader=yaml.FullLoader
                )
                if self._values[file] is None:
                    self._values[file] = {}

        return self._values

    def _dict_merge(self, a, b, path=None):
        if path is None:
            path = []
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    self._dict_merge(a[key], b[key], path + [str(key)])
            else:
                a[key] = b[key]
        return a

    @property
    def combined_values(self):
        combined = {}
        for filepath, data in self.values.items():
            combined = self._dict_merge(dict(data), dict(combined))
        return combined
