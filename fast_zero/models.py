from sqlalchemy.orm import registry


table_registry = registry()


@table_registry.mapped_as_dataclass
