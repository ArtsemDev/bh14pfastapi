from datetime import datetime, UTC

from sqlalchemy import (
    Column,
    VARCHAR,
    CheckConstraint,
    TIMESTAMP,
    String,
    BOOLEAN,
    BIGINT,
    ForeignKey,
    inspect, INT, create_engine,
)
from sqlalchemy.orm import relationship

from src.models import Base

__all__ = [
    "Tag",
    "Topic",
    "TopicTag",
]


# TopicTag = Table(
#     "blog_topic_tag",
#     Base.metadata,
#     Column(
#         "tag_id",
#         BIGINT,
#         ForeignKey("blog_tag.id", onupdate="CASCADE", ondelete="RESTRICT"),
#         primary_key=True,
#         index=True
#     ),
#     Column(
#         "topic_id",
#         BIGINT,
#         ForeignKey("blog_topic.id", onupdate="CASCADE", ondelete="RESTRICT"),
#         primary_key=True,
#         index=True
#     ),
# )


class TopicTag(Base):
    tag_id = Column(
        INT,
        ForeignKey(
            column="blog_tag.id",
            ondelete="RESTRICT",
            onupdate="CASCADE"
        ),
        primary_key=True,
        index=True
    )
    topic_id = Column(
        INT,
        ForeignKey(
            column="blog_topic.id",
            ondelete="RESTRICT",
            onupdate="CASCADE"
        ),
        primary_key=True,
        index=True
    )


class Tag(Base):
    __table_args__ = (
        CheckConstraint(sqltext="length(name) >= 2"),
    )

    name = Column(
        VARCHAR(length=32),
        nullable=False,
        unique=True,
    )

    topics = relationship(
        argument="Topic",
        secondary=inspect(TopicTag).local_table,
        back_populates="tags"
    )

    def __str__(self) -> str:
        return self.name


class Topic(Base):
    __table_args__ = (
        CheckConstraint(sqltext="length(title) >= 2"),
    )

    title = Column(
        VARCHAR(length=128),
        nullable=False,
    )
    slug = Column(
        VARCHAR(length=128),
        nullable=False,
        unique=True
    )
    date_created = Column(
        TIMESTAMP,
        default=lambda: datetime.now(tz=UTC),
        nullable=False
    )
    body = Column(String, nullable=False)
    is_published = Column(BOOLEAN, nullable=False, default=False)

    tags = relationship(
        argument="Tag",
        secondary=inspect(TopicTag).local_table,
        back_populates="topics",
    )
