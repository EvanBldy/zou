import tomlkit
import semver
import email.utils
import spdx_license_list
import zipfile
import importlib
import importlib.util
import sys
import os
import traceback

from pathlib import Path
from flask import current_app
from alembic import command
from alembic.config import Config


from pathlib import Path
from collections.abc import MutableMapping


class PluginManifest(MutableMapping):
    def __init__(self, data):
        super().__setattr__("data", data)
        self.validate()

    @classmethod
    def from_plugin_path(cls, path):
        path = Path(path)
        if path.is_dir():
            return cls.from_file(path / "manifest.toml")
        elif zipfile.is_zipfile(path):
            with zipfile.ZipFile(path) as z:
                with z.open("manifest.toml") as f:
                    data = tomlkit.load(f)
            return cls(data)
        else:
            raise ValueError(f"Invalid plugin path: {path}")

    @classmethod
    def from_file(cls, path):
        with open(path, "rb") as f:
            data = tomlkit.load(f)
        return cls(data)

    def write_to_path(self, path):
        path = Path(path)
        with open(path / "manifest.toml", "w", encoding="utf-8") as f:
            tomlkit.dump(self.data, f)

    def validate(self):
        semver.Version.parse(str(self.data["version"]))
        spdx_license_list.LICENSES[self.data["license"]]
        if "maintainer" in self.data:
            name, email_addr = email.utils.parseaddr(self.data["maintainer"])
            self.data["maintainer_name"] = name
            self.data["maintainer_email"] = email_addr

    def to_model_dict(self):
        return {
            "plugin_id": self.data["id"],
            "name": self.data["name"],
            "description": self.data.get("description"),
            "version": str(self.data["version"]),
            "maintainer_name": self.data.get("maintainer_name"),
            "maintainer_email": self.data.get("maintainer_email"),
            "website": self.data.get("website"),
            "license": self.data["license"],
        }

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return f"<PluginManifest {self.data!r}>"

    def __getattr__(self, attr):
        try:
            return self.data[attr]
        except KeyError:
            raise AttributeError(f"'PluginManifest' has no attribute '{attr}'")

    def __setattr__(self, attr, value):
        if attr == "data":
            super().__setattr__(attr, value)
        else:
            self.data[attr] = value


def load_plugin(app, plugin_path, init_plugin=True):
    """
    Load a plugin from the plugin folder.
    """
    plugin_path = Path(plugin_path)
    manifest = PluginManifest.from_plugin_path(plugin_path)

    plugin_module = importlib.import_module(manifest["id"])
    if init_plugin and hasattr(plugin_module, "init_plugin"):
        plugin_module.init_plugin(app, manifest)

    return plugin_module


def load_plugins(app):
    """
    Load plugins from the plugin folder.
    """
    plugin_folder = Path(app.config["PLUGIN_FOLDER"])
    abs_plugin_path = str(plugin_folder.absolute())
    if abs_plugin_path not in sys.path:
        sys.path.insert(0, abs_plugin_path)

    if plugin_folder.exists:
        for plugin_id in os.listdir(plugin_folder):
            try:
                load_plugin(app, plugin_folder / plugin_id)
                app.logger.info(f"Plugin {plugin_id} loaded.")
            except ImportError as e:
                app.logger.error(f"Plugin {plugin_id} failed to import: {e}")
            except Exception as e:
                app.logger.error(
                    f"Plugin {plugin_id} failed to initialize: {e}"
                )
                app.logger.debug(traceback.format_exc())

    if abs_plugin_path in sys.path:
        sys.path.remove(abs_plugin_path)


def migrate_plugin_db(plugin_path, message):
    """
    Generates Alembic migration files in path/migrations.
    """
    plugin_path = Path(plugin_path).absolute()
    models_path = plugin_path / "models.py"

    if not models_path.exists():
        raise FileNotFoundError(f"'models.py' not found in '{plugin_path}'")

    manifest = PluginManifest.from_plugin_path(plugin_path)

    module_name = f"_plugin_models_{manifest['id']}"
    spec = importlib.util.spec_from_file_location(module_name, models_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load 'models.py' from '{plugin_path}'")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
        migrations_dir = plugin_path / "migrations"
        versions_dir = migrations_dir / "versions"
        versions_dir.mkdir(parents=True, exist_ok=True)

        alembic_cfg = Config()
        alembic_cfg.config_file_name = str(plugin_path / "alembic.ini")
        alembic_cfg.set_main_option("script_location", str(migrations_dir))
        alembic_cfg.set_main_option(
            "sqlalchemy.url", current_app.config["SQLALCHEMY_DATABASE_URI"]
        )

        command.revision(alembic_cfg, autogenerate=True, message=message)
    finally:
        del sys.modules[module_name]


def run_plugin_migrations(plugin_path, plugin):
    """
    Run plugin migrations.
    """
    plugin_path = Path(plugin_path)

    alembic_cfg = Config()
    alembic_cfg.config_file_name = str(plugin_path / "alembic.ini")
    alembic_cfg.set_main_option(
        "script_location", str(plugin_path / "migrations")
    )
    alembic_cfg.set_main_option(
        "sqlalchemy.url", current_app.config["SQLALCHEMY_DATABASE_URI"]
    )

    command.upgrade(alembic_cfg, "head")

    script = command.ScriptDirectory.from_config(alembic_cfg)
    head_revision = script.get_current_head()

    plugin.revision = head_revision

    return head_revision


def downgrade_plugin_migrations(plugin_path):
    """
    Downgrade plugin migrations to base.
    """
    plugin_path = Path(plugin_path)
    manifest = PluginManifest.from_plugin_path(plugin_path)

    alembic_cfg = Config()
    alembic_cfg.config_file_name = str(plugin_path / "alembic.ini")
    alembic_cfg.set_main_option(
        "script_location", str(plugin_path / "migrations")
    )
    alembic_cfg.set_main_option(
        "sqlalchemy.url", current_app.config["SQLALCHEMY_DATABASE_URI"]
    )

    try:
        command.downgrade(alembic_cfg, "base")
    except Exception as e:
        current_app.logger.warning(
            f"Downgrade failed for plugin {manifest.id}: {e}"
        )
