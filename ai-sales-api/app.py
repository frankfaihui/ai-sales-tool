from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes import health_check, get_sales_pitches, login, create_sales_pitch, delete_sales_pitch
from config import Config
from mongo import mongo

# ------------------------------- set up app and configuration -------------------------------
def create_app(config_class=Config):
    app = Flask(__name__)
    # for development, allow all origins
    CORS(app, resources={r"/*": {"origins": "*"}})

    # load configuration
    app.config.from_object(config_class)

    # Setup mongo
    mongo.init_app(app)

    # Setup the Flask-JWT
    JWTManager(app)

    return app

app = create_app()

# ------------------------------- set up routes -------------------------------
app.add_url_rule('/', 'health_check', health_check, methods=['GET'])
app.add_url_rule('/login', 'login', login, methods=['POST'])

# ------------------------------- sales pitches routes are protected -------------------------------
app.add_url_rule('/sales-pitches', 'get_sales_pitches', get_sales_pitches, methods=['GET'])
app.add_url_rule('/sales-pitches', 'create_sales_pitch', create_sales_pitch, methods=['POST'])
app.add_url_rule('/sales-pitches/<string:id>', 'delete_sales_pitch', delete_sales_pitch, methods=['DELETE'])

# ------------------------------- start application -------------------------------
if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
