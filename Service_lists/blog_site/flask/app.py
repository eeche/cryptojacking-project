from flask import Flask, request, jsonify
import boto3
import psycopg2
import os

app = Flask(__name__)

# PostgreSQL 연결 설정
DATABASE_URL = os.getenv('DATABASE_URL')

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# S3 연결 설정
s3 = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                  aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

@app.route('/')
def home():
    return "Welcome to the blog site!"

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    s3.upload_fileobj(file, 'your-bucket-name', file.filename)
    return "File uploaded!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

