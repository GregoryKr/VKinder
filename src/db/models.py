from typing import Self

import sqlalchemy as sq
from sqlalchemy.orm import relationship

from .common import BaseModel, session


class User(BaseModel):
    __tablename__ = "users"

    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer, unique=True, nullable=False)
    first_name = sq.Column(sq.String)
    last_name = sq.Column(sq.String)
    sex = sq.Column(sq.Integer)
    home_town = sq.Column(sq.String)
    home_town_id = sq.Column(sq.Integer)
    age = sq.Column(sq.Integer)

    def save(self) -> Self:
        session.add(self)
        session.commit()
        return self

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class FoundUser(BaseModel):
    __tablename__ = "found_users"

    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer, unique=True, nullable=False)
    photos = sq.Column(sq.String)
    first_name = sq.Column(sq.String)
    last_name = sq.Column(sq.String)
    user_id = sq.Column(sq.Integer, sq.ForeignKey("users.id"), nullable=False)
    user = relationship("User", backref="found_users")

    def save(self) -> Self:
        session.add(self)
        session.commit()
        return self

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
