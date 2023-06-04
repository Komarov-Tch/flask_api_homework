import datetime
import sqlalchemy
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()
adress = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@127.0.0.1:5431/{os.getenv('POSTGRES_DB')}"
engine = create_engine(adress)
Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)


class User(Base):
    __tablename__ = 'users'

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )
    username = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False
    )
    email = sqlalchemy.Column(
        sqlalchemy.String,
        index=True,
        unique=True,
        nullable=False
    )
    hashed_password = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False
    )
    news = relationship("News", back_populates='user')

    def __str__(self):
        return f'{self.id}, {self.username}, {self.email}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class News(Base):
    __tablename__ = 'news'

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )
    title = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False
    )
    content = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=True
    )
    create_date = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=datetime.datetime.now
    )
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('users.id'))
    user = relationship('User')


Base.metadata.create_all()
