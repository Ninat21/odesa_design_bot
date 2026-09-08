import importlib.util
from pathlib import Path
from unittest import TestCase, mock

from sqlalchemy import Column, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.dialects import postgresql

import app.database.models  # noqa: F401
from app.database.database import Base


def load_revision(module_name: str, filename: str):
    path = Path(__file__).parents[1] / "alembic" / "versions" / filename
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load migration {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


initial_schema = load_revision(
    "initial_schema",
    "e27eb129e081_initial_schema.py",
)
message_sync = load_revision(
    "message_sync",
    "a62f1bf37d4c_sync_message_model.py",
)
profile_facts = load_revision(
    "profile_facts",
    "c91d38a72f44_add_profile_facts.py",
)


class MigrationRecorder:
    def __init__(self):
        self.tables: dict[str, dict[str, Column]] = {}
        self.unique_constraints: set[tuple[str, str | None, tuple[str, ...]]] = set()
        self.indexes: set[tuple[str, str, tuple[str, ...], bool]] = set()
        self.foreign_keys: set[
            tuple[str, tuple[str, ...], tuple[str, ...], str | None]
        ] = set()

    def create_table(self, table_name, *items, **_kwargs):
        self.tables[table_name] = {
            item.name: item for item in items if isinstance(item, Column)
        }
        for item in items:
            if isinstance(item, UniqueConstraint):
                self.unique_constraints.add(
                    (
                        table_name,
                        item.name,
                        tuple(str(column) for column in item._pending_colargs),
                    )
                )
            if isinstance(item, ForeignKeyConstraint):
                self.foreign_keys.add(
                    (
                        table_name,
                        tuple(str(column) for column in item._pending_colargs),
                        tuple(element._colspec for element in item.elements),
                        item.ondelete,
                    )
                )

    def add_column(self, table_name, column):
        self.tables[table_name][column.name] = column

    def get_bind(self):
        return self

    def get_columns(self, table_name):
        return [{"name": name} for name in self.tables[table_name]]

    def get_unique_constraints(self, table_name):
        return [
            {"name": name, "column_names": list(columns)}
            for constraint_table, name, columns in self.unique_constraints
            if constraint_table == table_name
        ]

    def execute(self, *_args, **_kwargs):
        return None

    def alter_column(self, *_args, **_kwargs):
        return None

    def create_unique_constraint(self, name, table_name, columns, **_kwargs):
        self.unique_constraints.add((table_name, name, tuple(columns)))

    def create_index(
        self,
        name,
        table_name,
        columns,
        unique=False,
        **_kwargs,
    ):
        self.indexes.add((table_name, name, tuple(columns), unique))


def column_signature(column: Column) -> tuple[str, bool]:
    column_type = column.type.compile(dialect=postgresql.dialect())
    return column_type, column.nullable


class MigrationContractTest(TestCase):
    def test_migrations_create_all_model_columns(self):
        recorder = MigrationRecorder()
        original_initial_op = initial_schema.op
        original_sync_op = message_sync.op
        original_profile_facts_op = profile_facts.op
        initial_schema.op = recorder
        message_sync.op = recorder
        profile_facts.op = recorder

        try:
            initial_schema.upgrade()
            with mock.patch.object(message_sync.sa, "inspect", return_value=recorder):
                message_sync.upgrade()
            profile_facts.upgrade()
        finally:
            initial_schema.op = original_initial_op
            message_sync.op = original_sync_op
            profile_facts.op = original_profile_facts_op

        model_tables = dict(Base.metadata.tables)
        self.assertEqual(set(recorder.tables), set(model_tables))

        for table_name, table in model_tables.items():
            self.assertEqual(
                set(recorder.tables[table_name]),
                set(table.columns.keys()),
                f"Migration columns differ from model {table_name}",
            )
            for column in table.columns:
                self.assertEqual(
                    column_signature(recorder.tables[table_name][column.name]),
                    column_signature(column),
                    f"Migration definition differs for {table_name}.{column.name}",
                )

        model_unique_constraints = {
            (
                table.name,
                constraint.name,
                tuple(column.name for column in constraint.columns),
            )
            for table in model_tables.values()
            for constraint in table.constraints
            if isinstance(constraint, UniqueConstraint)
        }
        self.assertEqual(recorder.unique_constraints, model_unique_constraints)

        model_indexes = {
            (
                table.name,
                index.name,
                tuple(column.name for column in index.columns),
                index.unique,
            )
            for table in model_tables.values()
            for index in table.indexes
        }
        self.assertEqual(recorder.indexes, model_indexes)

        model_foreign_keys = {
            (
                table.name,
                tuple(column.name for column in constraint.columns),
                tuple(element.target_fullname for element in constraint.elements),
                constraint.ondelete,
            )
            for table in model_tables.values()
            for constraint in table.constraints
            if isinstance(constraint, ForeignKeyConstraint)
        }
        self.assertEqual(recorder.foreign_keys, model_foreign_keys)
