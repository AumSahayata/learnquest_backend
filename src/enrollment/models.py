from datetime import datetime
import uuid
from sqlmodel import Field, SQLModel, Column
import sqlalchemy.dialects.postgresql as pg

class Enrollment(SQLModel, table=True):
    __tablename__="enrollment"
    user_uid: uuid.UUID = Field(
        sa_column = Column(
            pg.UUID,
            nullable = False,
            primary_key = True,
            default = uuid.uuid4
        )
    )
    course_uid: uuid.UUID = Field(
        sa_column = Column(
            pg.UUID,
            nullable = False,
            primary_key = True,
            default = uuid.uuid4
        )
    )
    enrollment_date: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    progress: float = Field(default=0.0)