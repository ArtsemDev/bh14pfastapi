from sqlalchemy import Column, VARCHAR, CHAR

from src.models import Base


class User(Base):
    email = Column(VARCHAR(length=128), nullable=False, unique=True)
    password = Column(CHAR(length=60), nullable=False)

    def __str__(self) -> str:
        return self.email
