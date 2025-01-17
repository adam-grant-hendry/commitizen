from __future__ import annotations

from pathlib import Path

import yaml

from commitizen.git import smart_open

from .base_config import BaseConfig


class YAMLConfig(BaseConfig):
    def __init__(self, *, data: bytes | str, path: Path | str):
        super(YAMLConfig, self).__init__()
        self.is_empty_config = False
        self._parse_setting(data)
        self.add_path(path)

    def init_empty_config_content(self):
        with smart_open(self.path, "a", encoding=self.encoding) as json_file:
            yaml.dump({"commitizen": {}}, json_file, explicit_start=True)

    def _parse_setting(self, data: bytes | str) -> None:
        """We expect to have a section in cz.yaml looking like

        ```
        commitizen:
          name: cz_conventional_commits
        ```
        """
        doc = yaml.safe_load(data)
        try:
            self.settings.update(doc["commitizen"])
        except (KeyError, TypeError):
            self.is_empty_config = True

    def set_key(self, key, value):
        """Set or update a key in the conf.

        For now only strings are supported.
        We use to update the version number.
        """
        with open(self.path, "rb") as yaml_file:
            parser = yaml.load(yaml_file, Loader=yaml.FullLoader)

        parser["commitizen"][key] = value
        with smart_open(self.path, "w", encoding=self.encoding) as yaml_file:
            yaml.dump(parser, yaml_file, explicit_start=True)

        return self
