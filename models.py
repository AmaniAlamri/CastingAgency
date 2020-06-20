import os
from sqlalchemy import Column, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy
import json

project_dir = os.path.dirname(os.path.abspath(__file__))

db = SQLAlchemy()


def setup_db(app, database_name):
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}".format(os.path.join(
        project_dir, database_name))
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


class Movie(db.Model):
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    title = Column(String(80), nullable=False)
    release_date = Column(DateTime(), nullable=False)
    actors = db.relationship("MovieActor", back_populates="movie")

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())


class Actor(db.Model):
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    name = Column(String(80), nullable=False)
    age = Column(Integer(), nullable=True, default=30)
    gender = Column(String(80), nullable=True, default="None")
    movies = db.relationship("MovieActor", back_populates="actor")

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())


class MovieActor(db.Model):
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    movie_id = Column(Integer(), db.ForeignKey(Movie.id))
    actor_id = Column(Integer(), db.ForeignKey(Actor.id))
    movie = db.relationship("Movie", back_populates="actors")
    actor = db.relationship("Actor", back_populates="movies")

    def format(self):
        return {
            'id': self.id,
            'movie_id': self.movie_id,
            'actor_id': self.actor_id
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())
