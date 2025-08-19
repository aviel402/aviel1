from flask import Flask, request, Response
from urllib.parse import urlencode

# =======================================================
#             חלק A (עם תיקון Cookie)
# =======================================================

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def flask_controller():
    # קבלת הנתונים כמו קודם
    all_params = request.form if request.form else request.args
    
    # הפעלת הלוגיקה
    final_response_string = yemot_service(all_params)

    # יצירת אובייקט התגובה המלא
    response = Response(final_response_string, mimetype='text/plain; charset=UTF-8')

    # **** כאן נמצא התיקון הקריטי ****
    # נשמור באופן מפורש את מזהה השיחה ב-Cookie
    # כדי לוודא שימות המשיח ממשיכה את אותה שיחה
    if 'ApiCallId' in all_params:
        response.set_cookie('session', all_params['ApiCallId'])
        
    return response

# =======================================================
#             חלק B (כמו קודם)
# =======================================================
def yemot_service(request_params):
    x = request_params.get("x")
    if x == "1":
        return a(request_params)
    return "id_list_message=t-פעולה לא מוגדרת"

# =======================================================
#        חלק C (כמו קודם, עם התיקון של STEP)
# =======================================================
def a(params):
    step = params.get("step", params.get("STEP", "1"))

    # שלב 1: בקשת המספר הראשון
    if step == "1":
        prompt = "t-ברוך הבא למחשבון, אנא הקש את המספר הראשון"
        return_path_params = urlencode({'x': '1', 'step': '2'})
        return_path = f"/?{return_path_params}"
        return f"read={prompt}=num1,,,{return_path}"
        
    # שלב 2: בקשת פעולה
    elif step == "2":
        num1_from_user = params.get("num1")
        prompt = "t-אנא הקש פעולה"
        return_path_params = urlencode({'x': '1', 'step': '3', 'saved_num1': num1_from_user})
        return_path = f"/?{return_path_params}"
        return f"read={prompt}=op,,1,1,{return_path}"
    
    # שלב 3: בקשת מספר שני
    elif step == "3":
        num1_saved = params.get("saved_num1")
        op_saved = params.get("op")
        prompt = "t-אנא הקש מספר שני"
        return_path_params = urlencode({'x': '1', 'step': '4', 'saved_num1': num1_saved, 'saved_op': op_saved})
        return_path = f"/?{return_path_params}"
        return f"read={prompt}=num2,,,{return_path}"
        
    # שלב 4: ביצוע החישוב
    elif step == "4":
        a_str, b_str, c_str = params.get("saved_num1"), params.get("saved_op"), params.get("num2")
        d = ""
        try:
            a, b, c = float(a_str), b_str, float(c_str)
            if b == '1': d = a + c
            # ... שאר הלוגיקה ...
            else: d = "פעולה לא חוקית"
        except:
            d = "שגיאה"
        return f"id_list_message=t-התוצאה היא {d}"

    return "id_list_message=t-שגיאה"