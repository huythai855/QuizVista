# implement APP Runner here

import flask
import flask_cors
import os
from config.environment import get_settings
from backend_service.api.route import api_blueprint



def create_app():
    app = flask.Flask(__name__)
    flask_cors.CORS(app)
    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app


if __name__ == "__main__":
    settings = get_settings()
    app = create_app()
    app.run(port=settings.BACKEND_PORT)