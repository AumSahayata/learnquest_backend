from datetime import datetime
from sqlmodel import Field, SQLModel, Column
import sqlalchemy.dialects.postgresql as pg
import uuid

class Content(SQLModel, table=True):
    __tablename__ = "content"
    content_uid: uuid.UUID = Field(
        sa_column = Column(
            pg.UUID,
            nullable = False,
            primary_key = True,
            default = uuid.uuid4
        )
    )
    course_uid: uuid.UUID = Field(foreign_key="courses.course_uid", default=None)
    content_title: str
    content_description: str
    content_type: str
    content_data: str
    content_order: int
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))