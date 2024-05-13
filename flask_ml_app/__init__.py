from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # db.init_app(app)
    # from .views import main_views, question_views, answer_views
    # app.register_blueprint(main_views.bp)
    from .views import main_views

    app.register_blueprint(main_views.bp)

    return app