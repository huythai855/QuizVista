from flask import Blueprint

from .classes.create_class.route import api_create_classes

api_blueprint = Blueprint('api', __name__)



api_blueprint.register_blueprint(api_create_classes, url_prefix="/classes")
