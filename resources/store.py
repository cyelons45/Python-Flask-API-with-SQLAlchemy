
from flask_restful import reqparse, Resource
from flask import Flask, request
from flask_restful import reqparse, abort, Api
from flask_jwt import jwt_required, current_identity
from models.store import StoreModel
# from security import authenticate, identity


class Store(Resource):
    @jwt_required()
    def get(self, name):
        pass
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": "Store not found"}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": f"An store with name {name} already exists"}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except Exception as e:
            return {"message": "An error occured while creating the store  "+str(e)}, 500
        return store.json(),  201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {"message": "Store deleted"}


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}
