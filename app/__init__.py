from flask  import Flask,url_for
# from flask_bootstrap import  Bootstrap
def create_app():
    app = Flask(__name__, static_folder='static')
    # pip bootstrap = Bootstrap(app)
    return app