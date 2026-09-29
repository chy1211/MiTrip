from flask import Flask
from flask_cors import CORS
from config import API_HOST, API_PORT, DEBUG
from auth import auth_bp
from restaurant import res_bp
from attraction import attr_bp
from hotel import hot_bp
from reviews import rev_bp
from schedule import sch_bp
from explore import exp_bp
from questionnaire import qes_bp


app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

app.register_blueprint(auth_bp)
app.register_blueprint(res_bp)
app.register_blueprint(attr_bp)
app.register_blueprint(hot_bp)
app.register_blueprint(rev_bp)
app.register_blueprint(sch_bp)
app.register_blueprint(exp_bp)
app.register_blueprint(qes_bp)


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT, debug=DEBUG)
