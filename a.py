from flask import Flask, request, Response
from urllib.parse import urlencode

# =======================================================
#             חלק A (כפי שהגדרת)
# =======================================================
app = Flask(__name__)
@app.route('/', methods=['POST', 'GET'])
def flask_controller():
    all_params = request.values
    final_response_string = yemot_service(all_params)
    return Response(final_response_string, mimetype='text/plain; charset=UTF-8')

# =======================================================
#             חלק B (כפי שהגדרת)
# =======================================================
def yemot_service(request_params):
    x = request_params.get("x")
    if x == "1":
        return a_debugger(request_params)
    return "id_list_message=t-פעולה לא מוגדרת (x was not 1)"

# =======================================================
#        חלק C (פונקציה 'a') - גרסת בלש פשוטה
# =======================================================
def a_debugger(params):
    
    # 1. נדפיס את כל מה שקיבלנו, כדי לראות את האמת
    print("--- NEW REQUEST RECEIVED ---")
    print(f"FULL PARAMS: {params}")
    
    # 2. נבדוק באיזה שלב אנחנו *באמת*
    step = params.get("step", params.get("STEP", "1"))
    print(f"DETECTED STEP: {step}")

    # --- שלב 1: אם זו הפנייה הראשונה ---
    if step == "1":
        print("LOGIC: This is STEP 1. Preparing command for STEP 2.")
        
        prompt = "t-זהו ניסוי. אנא הקש את הספרה 5"
        # נבנה את כתובת החזרה ונראה אותה בלוג
        return_path = f"/?x=1&step=2"
        print(f"LOGIC: Return path is: {return_path}")
        
        # נחזיר את פקודת ה-read
        return f"read={prompt}=debug_input,,1,1,{return_path}"
        
    # --- שלב 2: אם זו הפנייה השנייה ---
    else:
        print("LOGIC: This should be STEP 2.")
        user_input = params.get("debug_input")
        return f"id_list_message=t-הגעת לשלב השני. הקלט היה {user_input}"