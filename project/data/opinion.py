import sqlalchemy
from .db_session import SqlAlchemyBase


class Opinion(SqlAlchemyBase):
    __tablename__ = 'opinions'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    opinion = sqlalchemy.Column(sqlalchemy.String)
    id_user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    id_book = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('books.id'))
