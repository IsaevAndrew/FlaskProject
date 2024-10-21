import sqlalchemy
from .db_session import SqlAlchemyBase


class Wishlist(SqlAlchemyBase):
    __tablename__ = 'wishlists'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    id_book = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('books.id'))
