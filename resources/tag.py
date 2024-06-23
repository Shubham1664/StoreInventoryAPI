from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from models import TagsModel, StoreModel
from shcemas import TagSchema, TagUpdateSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("Tags", __name__,description="Operations on Tags")

@blp.route("/store/<string:store_id>/tags")
class Tag(MethodView):
    
    @blp.response(200, TagSchema)
    def get(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()
    
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        tag = TagSchema(**tag_data, store_id = store_id)
        if TagsModel.query.filter(TagsModel.store_id == store_id,TagsModel.name == tag_data["name"]).first:
            abort(400, message="A tag with that name already exists")
            
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=e)
        
        return tag

@blp.route("/tag/<string:tag_id>")
class TagList(MethodView):
    
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagsModel.query.get_or_404(tag_id)
        return tag