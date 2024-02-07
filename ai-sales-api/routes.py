from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from mongo import mongo
from config import Config
from langchain.prompts.chat import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from datetime import datetime
from bson.objectid import ObjectId

# create an instance of the ChatOpenAI
chat_model = ChatOpenAI(openai_api_key=Config.OPENAI_API_KEY)

def health_check():
    """
    Health check endpoint.
    """
    return jsonify({'message': 'Welcome to the AI Sales API', 'status': 'OK'})

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

@jwt_required()
def get_sales_pitches():
    """
    Get a list of the latest sales pitches.
    """
    # Access the identity of the current user
    current_user = get_jwt_identity()

    items = list(mongo.db.sales_pitches.find({'created_by': current_user}).sort('timestamp', -1).limit(10))
    return jsonify({'data': list(map(convert_id, items))})

def convert_id(item):
    item['_id'] = str(item['_id'])
    return item

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

    result = mongo.db.sales_pitches.insert_one(new_item)
    return jsonify({'_id': str(result.inserted_id), 'content': new_item['content']}), 201

@jwt_required()
def delete_sales_pitch(id):
    """
    Delete a sales pitch by ID.
    """

    current_user = get_jwt_identity()

    result = mongo.db.sales_pitches.delete_one({'_id': ObjectId(id), 'created_by': current_user})

    if result.deleted_count > 0:
        return jsonify({'message': 'Item deleted successfully'}), 200
    else:
        return jsonify({'message': 'Item not found'}), 404
