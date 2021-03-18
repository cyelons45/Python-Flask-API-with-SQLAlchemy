import sqlite3
from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='Username is required'
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='Password is required'
                        )

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.findbyusername(data['username']):
            return {"message": "A user with this username already exist"}, 400
        user = UserModel(**data)
        user.save_to_db()
        return {"message": "User created successfully"}


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        user.delete_from_db()
        return {"message": "User deleted"}


# if __name__ == '__main__':
#     # res =UserModel.findbyusername('jose')
#     res = UserModel.findbyid(3)
#     print(res.__dict__)
