from alembic import context
from sqlalchemy import create_engine, pool
import importlib.util
import sys
from pathlib import Path
from zou.app import db
from zou.app.utils.plugins import PluginManifest

plugin_path = Path(__file__).resolve().parents[1]
models_path = plugin_path / "models.py"
manifest = PluginManifest.from_plugin_path(plugin_path)

module_name = f"_plugin_models_{manifest['id']}"
spec = importlib.util.spec_from_file_location(module_name, models_path)
module = importlib.util.module_from_spec(spec)
sys.modules[module_name] = module
spec.loader.exec_module(module)

target_metadata = db.metadata

# Database URL (passed by Alembic)
config = context.config
url = config.get_main_option("sqlalchemy.url")


def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table" and name == "alembic_version":
        return False  # ignore la table alembic_version principale
    return True


def run_migrations_online():
    connectable = create_engine(url, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table=f"alembic_version_{manifest['id']}",
            compare_type=True,
            include_object=include_object,
        )
        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
