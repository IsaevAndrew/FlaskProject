import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Avtor(SqlAlchemyBase):
    __tablename__ = 'avtors'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    books = orm.relation("Book", back_populates='avtor')
