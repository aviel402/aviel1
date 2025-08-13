from flask import Flask, request

app = Flask(__name__)

# A
@app.route('/', methods=['POST', 'GET'])
def flask_controller():
    all_params = request.values
    yemot_service(all_params)
    return ""











# B
def yemot_service(request_params):
    x = request_params.get("x")
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #











# C
def core_logic():
    pass
