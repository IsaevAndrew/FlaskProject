import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Genre(SqlAlchemyBase):
    __tablename__ = 'genres'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    books = orm.relation("Book", back_populates='genre')
