from flask import Flask, jsonify, request
from flask.views import MethodView
from data.models.models import Session, User, News
from data.shema import VALIDATION_CLASS, CreateUser, PatchUser
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)


class HttpError(Exception):

    def __init__(self, status_code: int, message: dict | list | str):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def http_error_handler(error: HttpError):
    error_message = {
        'status': 'error',
        'description': error.message,
        }
    response = jsonify(error_message)
    response.status_code = error.status_code
    return response


def get_user(session: Session, user_id: int):
    user = session.get(User, user_id)
    if user is None:
        raise HttpError(404, message="user is not found")
    return user


def get_news(session: Session, news_id: int):
    news = session.get(News, news_id)
    if news is None:
        raise HttpError(404, message="news is not found")
    return news


def validate_json(json_data: dict, validation_model: VALIDATION_CLASS):
    try:
        model_obj = validation_model(**json_data)
        model_obj_dict = model_obj.dict()
    except ValidationError as err:
        raise HttpError(400, message=err.errors())
    return model_obj_dict


class UserView(MethodView):
    def get(self, user_id: int):
        with Session() as session:
            user = get_user(session, user_id)
            return jsonify({
                'id': user.id,
                'username': user.name,
            })

    def post(self):
        json_data = validate_json(request.json, CreateUser)
        with Session() as session:
            user = User()
            user.name = json_data['name']
            user.email = json_data['email']
            user.set_password(json_data['password'])
            session.add(user)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, message='such user exists')
            return jsonify({
                'id': user.id,
                'name': user.name,
                'email': user.email,

            })

    def patch(self, user_id: int):
        json_data = validate_json(request.json, PatchUser)
        with Session() as session:
            user = get_user(session, user_id)
            for field, value in json_data.items():
                setattr(user, field, value)
            session.add(user)
            session.commit()
            return jsonify({
                'id': user.id,
                'name': user.name,
            })

    def delete(self, user_id: int):
        with Session() as session:
            user = get_user(session, user_id)
            session.delete(user)
            session.commit()
            return jsonify({
                'status': 'success'
            })


class NewsView(MethodView):
    def get(self, news_id: int):
        with Session() as session:
            news = get_news(session, news_id)
            return jsonify({
                'id': news.id,
                'title': news.title,
                'content': news.content,
                'date': str(news.create_date),
                'user': news.user,
            })

    def post(self):
        ...

    def patch(self, news_id: int):
        json_data = request.json
        with Session() as session:
            news = get_news(session, news_id)
            for field, value in json_data.items():
                setattr(news, field, value)
            session.add(news)
            session.commit()
            return jsonify({
                'id': news.id,
                'title': news.title,
                'content': news.content,
                'date': str(news.create_date),
                'user': news.user,
            })

    def delete(self, news_id: int):
        with Session() as session:
            news = get_news(session, news_id)
            session.delete(news)
            session.commit()
            return jsonify({
                'status': 'success'
            })


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
