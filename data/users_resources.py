from data import db_session
from data.users import User
from flask import jsonify
from werkzeug.security import generate_password_hash
from flask_restful import reqparse, abort, Resource

db_session.global_init("db/users.db")


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        abort(404, message=f"User {user_id} not found")


def set_password(password):
    return generate_password_hash(password)


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        users = session.query(User).get(user_id)
        return jsonify({'users': users.to_dict(
            only=('id', 'name', 'pts', 'email'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        users = session.query(User).get(user_id)
        session.delete(users)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('role', required=True)
parser.add_argument('pts', required=True)
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('id', 'name', 'pts', 'role')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        users = User(
            name=args['name'],
            role=args['role'],
            pts=args['pts'],
            email=args['email'],
            hashed_password=set_password(args['password']),
        )
        session.add(users)
        session.commit()
        return jsonify({'success': 'OK'})