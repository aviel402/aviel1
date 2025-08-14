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
    if x == 1:
        a()
    #
    #
    #
    #
    #
    #
    #
    #
    #











#מחשבון
def a():
    print("-t ברוך הבא למחשבון, אנא הקש את המספר הראשון record_digits=yes")
    a = digits + 0
    print("-t אנא הקש פעולה, חיבור,1, חיסור, 2, כפל, 3, חילוק, 4,   record_digits=yes")
    b = digits + 0
    print("-t אנא הקש את המספר השני record_digits=yes")
    c = digits + 0
    if b == 1:
        d = a + c
    elif b == 2:
        d = a - c
    elif b == 3:
        d = a * c
    elif b == 4:
        if b != 0:
            d = a = c
        else:
            d = "אי אפשר לחלק באפס"
    else:
        d = "פעולה לא חוקית"
    print(f"-t התוצאה היא:{d}")


