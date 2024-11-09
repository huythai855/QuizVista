from flask import Blueprint

from .classes.create_new_class.route import api_create_classes
from .classes.list_all_classes.route import api_list_all_classes
from .classes.list_all_members.route import api_list_all_members
from .credentials.login.route import api_login
from .credentials.register.route import api_register
from .tests.create_new_test.route import api_create_new_test
from .tests.list_all_tests.route import api_list_all_tests
from .tests.get_test_detail.route import api_get_test_detail
from .tests.get_test_history.route import api_get_test_history

api_blueprint = Blueprint('api', __name__)

api_blueprint.register_blueprint(api_create_classes, url_prefix="/classes")
api_blueprint.register_blueprint(api_list_all_classes, url_prefix="/classes")
api_blueprint.register_blueprint(api_list_all_members, url_prefix="/classes")

api_blueprint.register_blueprint(api_login, url_prefix="/credentials")
api_blueprint.register_blueprint(api_register, url_prefix="/credentials")
api_blueprint.register_blueprint(api_create_new_test, url_prefix="/tests")
api_blueprint.register_blueprint(api_list_all_tests, url_prefix="/tests")
api_blueprint.register_blueprint(api_get_test_detail, url_prefix="/tests")
api_blueprint.register_blueprint(api_get_test_history, url_prefix="/tests")



