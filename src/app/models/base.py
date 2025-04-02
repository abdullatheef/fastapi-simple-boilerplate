# app/models/base.py
import uuid
from datetime import datetime
from sqlalchemy import inspect, Column, String, Boolean
from sqlalchemy.orm import aliased
from weakref import WeakValueDictionary
from ..core.db.database import Base
from sqlalchemy.dialects.postgresql import UUID


class MetaBaseModel(Base.__class__):
    def __init__(cls, *args):
        super().__init__(*args)
        cls.aliases = WeakValueDictionary()

    def __getitem__(cls, key):
        try:
            alias = cls.aliases[key]
        except KeyError:
            alias = aliased(cls)
            cls.aliases[key] = alias
        return alias

class BaseModel(Base, metaclass=MetaBaseModel):
    __abstract__ = True

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    is_deleted = Column(Boolean, default=False)

    print_filter = ()
    to_json_filter = ()

    def __repr__(self):
        return "%s(%s)" % (
            self.__class__.__name__,
            {column: value for column, value in self._to_dict().items() if column not in self.print_filter},
        )

    @property
    def json(self):
        return {
            column: value if not isinstance(value, datetime) else value.strftime("%Y-%m-%dT%H:%M:%S%z")
            for column, value in self._to_dict().items()
            if column not in self.to_json_filter
        }

    def _to_dict(self):
        return {column.key: getattr(self, column.key) for column in inspect(self.__class__).attrs}
