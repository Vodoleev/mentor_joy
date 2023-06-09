from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
app.app_context().push()

from auth import auth as auth_blueprint
from main import main as main_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
