import os

class Config:
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://127.0.0.1:27017/ai_sales_tool')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 'test_key')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'test_secret_key')
