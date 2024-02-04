from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from openai import OpenAI
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
# for development, allow all origins
CORS(app, resources={r"/*": {"origins": "*"}})

# load the environment variables
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 'test')
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://127.0.0.1:27017/ai_sales')

# connect to the mongo database
app.config['MONGO_URI'] = MONGO_URI
mongo = PyMongo(app)
db_sales_pitches = mongo.db.sales_pitches

# create an instance of the OpenAI API
client = OpenAI(
    api_key=OPENAI_API_KEY,
)

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({'message': 'Welcome to the AI Sales API', 'status': 'OK'})

# get a list of sales pitches
@app.route('/sales-pitches', methods=['GET'])
def get_sales_pitches():
    items = list(db_sales_pitches.find()
                 .sort('timestamp', -1)
                 .limit(10))

    return jsonify({'data': list(map(convert_id, items))})

def convert_id(item):
    item['_id'] = str(item['_id'])
    return item

# create a new sales pitch
@app.route('/sales-pitches', methods=['POST'])
def create_sales_pitch():
    body = request.json

    chat_completion = client.chat.completions.create(
        messages=[
            {
                'role': 'system',
                'content': f'Create a sales pitch for {body["product"]} targeting {body["audience"]}. Keep it under 100 words',
            }
        ],
        max_tokens=200,
        model='gpt-3.5-turbo',
    )

    new_item = {
        'product': body['product'],
        'audience': body['audience'],
        'content': chat_completion.choices[0].message.content,
        'timestamp': datetime.now().utcnow(),
    }

    result = db_sales_pitches.insert_one(new_item)
    return jsonify({'_id': str(result.inserted_id), 'content': new_item['content']}), 201

# delete a sales pitch
@app.route('/sales-pitches/<id>', methods=['DELETE'])
def delete_sales_pitch(id):
    result = db_sales_pitches.delete_one({'_id': ObjectId(id)})

    if result.deleted_count > 0:
        return jsonify({'message': 'Item deleted successfully'}), 200
    else:
        return jsonify({'message': 'Item not found'}), 404

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
