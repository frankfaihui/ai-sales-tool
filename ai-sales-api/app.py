from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from openai import OpenAI
from flask_cors import CORS
from datetime import datetime
import os
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from langchain.prompts.chat import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# ------------------------------- set up app and configuration -------------------------------

app = Flask(__name__)
# for development, allow all origins
CORS(app, resources={r"/*": {"origins": "*"}})

# load the environment variables
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 'test_key')
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://127.0.0.1:27017/ai_sales_tool')

# connect to the mongo database
app.config['MONGO_URI'] = MONGO_URI
mongo = PyMongo(app)
db_sales_pitches = mongo.db.sales_pitches

# create an instance of the OpenAI API
client = OpenAI(api_key=OPENAI_API_KEY)
chat_model = ChatOpenAI(openai_api_key=OPENAI_API_KEY)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'test_secret_key'
jwt = JWTManager(app)

# ------------------------------- router start -------------------------------

@app.route('/', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    """
    return jsonify({'message': 'Welcome to the AI Sales API', 'status': 'OK'})


@app.route('/sales-pitches', methods=['GET'])
@jwt_required()
def get_sales_pitches():
    """
    Get a list of the latest sales pitches.
    """
    # Access the identity of the current user
    current_user = get_jwt_identity()

    items = list(db_sales_pitches.find({'created_by': current_user}).sort('timestamp', -1).limit(10))
    return jsonify({'data': list(map(convert_id, items))})

def convert_id(item):
    item['_id'] = str(item['_id'])
    return item


@app.route('/sales-pitches', methods=['POST'])
@jwt_required()
def create_sales_pitch():
    """
    Create a new sales pitch using OpenAI Chat API.
    """
    body = request.json

    current_user = get_jwt_identity()

    template = "You are a creative assistant that create sales pitches for products"
    human_template = "Create a sales pitch for {product} targeting {audience} Keep it under 100 words"

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        ("human", human_template),
    ])

    messages = chat_prompt.format_messages(product="shampoo", audience="consumer")
    prediction = chat_model.predict_messages(messages)

    new_item = {
        'product': body['product'],
        'audience': body['audience'],
        'content': prediction.content,
        'created_by': current_user,
        'timestamp': datetime.now().utcnow(),
    }

    result = db_sales_pitches.insert_one(new_item)
    return jsonify({'_id': str(result.inserted_id), 'content': new_item['content']}), 201


@app.route('/sales-pitches/<id>', methods=['DELETE'])
@jwt_required()
def delete_sales_pitch(id):
    """
    Delete a sales pitch by ID.
    """

    current_user = get_jwt_identity()

    result = db_sales_pitches.delete_one({'_id': ObjectId(id), 'created_by': current_user})

    if result.deleted_count > 0:
        return jsonify({'message': 'Item deleted successfully'}), 200
    else:
        return jsonify({'message': 'Item not found'}), 404

@app.route('/login', methods=['POST'])
def login():
    """
    Login endpoint.
    """
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    # for demonstration purpose, authenticate any user
    if username and password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# ------------------------------- start application -------------------------------

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
