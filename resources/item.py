
from flask_restful import reqparse, Resource
from flask import Flask, request
from flask_restful import reqparse, abort, Api
from flask_jwt import jwt_required, current_identity
from models.item import ItemModel
# from security import authenticate, identity


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left blank'
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='Every item needs a store id'
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": f"An item with name {name} already exists"}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except Exception as e:
            return {"message": "Failed to insert data "+str(e)}, 500
        return item.json()

    def put(self, name):
        data = Item.parser.parse_args()
        # requestItem = request.get_json()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json, 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": "Item deleted"}


class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.find_all()]}
