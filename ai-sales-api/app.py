from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from openai import OpenAI
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
# for development, allow all origins
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['MONGO_URI'] = 'mongodb://localhost:27017/ai_sales'
mongo = PyMongo(app)

client = OpenAI(
    api_key='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',
)

@app.route('/sales-pitches', methods=['GET'])
def get_sales_pitches():
    items = list(mongo.db.sales_pitches.find().sort('timestamp', -1).limit(10))

    return jsonify({'data': list(map(convert_id, items))})

def convert_id(item):
    item['_id'] = str(item['_id'])
    return item

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

    result = mongo.db.sales_pitches.insert_one(new_item)
    return jsonify({'_id': str(result.inserted_id), 'content': new_item['content']}), 201


@app.route('/sales-pitches/<id>', methods=['DELETE'])
def delete_sales_pitch(id):
    result = mongo.db.sales_pitches.delete_one({'_id': ObjectId(id)})

    if result.deleted_count > 0:
        return jsonify({'message': 'Item deleted successfully'}), 200
    else:
        return jsonify({'message': 'Item not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=8080)
