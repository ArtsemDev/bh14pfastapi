import re

from sqlalchemy import Column, BIGINT, INT
from sqlalchemy.orm import DeclarativeBase, declared_attr

__all__ = ["Base"]


class Base(DeclarativeBase):
    id = Column(INT, primary_key=True)

    @declared_attr.directive
    def __tablename__(self):
        return re.sub(
            pattern=r"(?<!^)(?=[A-Z])",
            repl="_",
            string=self.__module__.split(".")[0] + self.__name__
        ).lower()
