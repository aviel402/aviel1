from flask import Flask, request, Response
from urllib.parse import urlencode

app = Flask(__name__)
@app.route('/', methods=['POST', 'GET'])
def diagnostic_tool():
    # שלב א': מתעדים הכל. תמיד.
    print("--- NEW YEMOT REQUEST RECEIVED ---")
    print(f"REQUEST METHOD: {request.method}") # נראה אם זה GET או POST
    # נבדוק את כל המקומות האפשריים שבהם הפרמטרים יכולים להיות
    print(f"PARAMS FROM 'form' (POST): {request.form.to_dict()}")
    print(f"PARAMS FROM 'args' (GET): {request.args.to_dict()}")

    # שלב ב': מאחדים את הפרמטרים למילון אחד, לא משנה איך הם הגיעו
    params = request.form if request.method == 'POST' else request.args
    step = params.get("step", "1")
    
    print(f"--- DIAGNOSTIC: Detected STEP is '{step}' ---")

    # שלב ג': לוגיקת הבדיקה הפשוטה
    if step == "1":
        print("--- DIAGNOSTIC: Executing STEP 1 logic. Preparing command for STEP 2.")
        prompt = "t-זהו מבחן תקשורת. אנא הקש את הספרה חמש"
        return_path = f"/?x=1&step=2"
        response_str = f"read={prompt}=test_input,,1,1,{return_path}"
    else: # step is "2" or something else
        user_input = params.get("test_input")
        print("--- DIAGNOSTIC: Executing STEP 2 logic.")
        response_str = f"id_list_message=t-הצלחה. הגעת לשלב השני. הקלט היה {user_input}&go_to_folder=hangup"
        
    print(f"--- DIAGNOSTIC: Sending back to Yemot: '{response_str}'")
    return Response(response_str, mimetype='text/plain')