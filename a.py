from flask import Flask, request, Response
import random

app = Flask(__name__)

@app.route('/yemot', methods=['POST', 'GET'])

params = request.values
print(params)
