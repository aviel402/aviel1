from flask import Flask, request, Response
from urllib.parse import urlencode

# =======================================================
#             חלק A (עם התיקון הקריטי)
# =======================================================

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def flask_controller():
    # **** התיקון המרכזי והחשוב ביותר נמצא כאן ****
    # נבדוק אם הנתונים הגיעו כטופס (POST), ואם לא, ניקח אותם מהכתובת (GET)
    all_params = request.form if request.form else request.args
    
    # מכאן והלאה, הכל ממשיך כרגיל
    final_response_string = yemot_service(all_params)
    return Response(final_response_string, mimetype='text/plain; charset=UTF-8')











# =======================================================
#             חלק B (נשאר כפי שהוא)
# =======================================================

def yemot_service(request_params):
    x = request_params.get("x")
    if x == "1":
        # קוראים לפונקציית המחשבון
        return a(request_params)
    
    return "id_list_message=t-פעולה לא מוגדרת"











# =======================================================
#        חלק C (המחשבון המלא)
# =======================================================
def a(params):
    
    step = params.get("step", params.get("STEP", "1"))

    # --- שלב 1: בקשת המספר הראשון ---
    if step == "1":
        prompt = "t-ברוך הבא למחשבון, אנא הקש את המספר הראשון"
        return_path = f"/?x=1&step=2"
        return f"read={prompt}=num1,,,{return_path}"
        
    # --- שלב 2: בקשת פעולה ---
    elif step == "2":
        num1_from_user = params.get("num1")
        prompt = "t-אנא הקש פעולה, 1 לחיבור, 2 לחיסור, 3 לכפל, 4 לחילוק, 5 לחזקה"
        return_path_params = urlencode({'x': '1', 'step': '3', 'saved_num1': num1_from_user})
        return_path = f"/?{return_path_params}"
        return f"read={prompt}=op,,1,1,{return_path}"

    # --- שלב 3: בקשת מספר שני ---
    elif step == "3":
        num1_saved = params.get("saved_num1")
        op_saved = params.get("op")
        prompt = "t-אנא הקש את המספר השני"
        return_path_params = urlencode({'x': '1', 'step': '4', 'saved_num1': num1_saved, 'saved_op': op_saved})
        return_path = f"/?{return_path_params}"
        return f"read={prompt}=num2,,,{return_path}"
        
    # --- שלב 4: ביצוע החישוב והשמעת התוצאה ---
    elif step == "4":
        a_str = params.get("saved_num1")
        b_str = params.get("saved_op")
        c_str = params.get("num2")
        d = ""
        
        try:
            a = float(a_str)
            b = b_str
            c = float(c_str)
            
            if b == '1': d = a + c
            elif b == '2': d = a - c
            elif b == '3': d = a * c
            elif b == '4':
                if c != 0: d = round(a / c, 2)
                else: d = "אי אפשר לחלק באפס"
            elif b == '5': d = a ** c
            else: d = "פעולה לא חוקית"
        except:
            d = "שגיאה בערכים שהוקשו"

        return f"id_list_message=t-התוצאה היא {d}"

    # אם מסיבה כלשהי הגענו לשלב לא מוכר
    return "id_list_message=t-שגיאה לא צפויה במערכת"