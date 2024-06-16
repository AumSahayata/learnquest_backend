from datetime import datetime
import uuid
from sqlmodel import Field, SQLModel, Column
import sqlalchemy.dialects.postgresql as pg

class Course(SQLModel, table = True):
    __tablename__ = "courses"
    course_uid: uuid.UUID = Field(
        sa_column = Column(
            pg.UUID,
            nullable = False,
            primary_key = True,
            default = uuid.uuid4
        )
    )
    course_name: str
    course_description: str
    course_creator: uuid.UUID = Field(foreign_key="users.uid", default=None)
    course_image: str = Field(default=None)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))