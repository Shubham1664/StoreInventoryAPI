from sqlite3 import IntegrityError
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from shcemas import StoreSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import StoreModel
from flask_jwt_extended import jwt_required
blp = Blueprint("stores", __name__, description = "Operation on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    
     @blp.response(200, StoreSchema)
     def get(self, store_id):
         store = StoreModel.query.get_or_404(store_id)
         return store
     
     def delete(self, store_id):
         store = StoreModel.query.get_or_404(store_id)
         db.session.delete(store)
         db.session.commit()
         return {"Message": "Store deleted successfully"}

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error while creating a new store in the database")
        except IntegrityError:
            abort(500,message="Store with the same name already exists.")
        return store, 201