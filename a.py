# קובץ: a.py
# מחשבון מלא: מספר ראשון, פעולה, מספר שני, חישוב

from flask import Flask, request, Response
from urllib.parse import urlencode

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def calculator_full_final():
    
    yemot_commands = []
    params = request.values
    
    print(f"Parameters received: {params}")
    
    step = params.get("step", "1")
    digits = params.get("digits", "") # הקלט הנוכחי

    # ------------------
    # שלב 1: קבלת המספר הראשון
    # ------------------
    if step == "1":
        if not digits: # אם זו שיחה ראשונה, בלי קלט
            return_path_params = urlencode({'step': '2'})
            return_path = f"/?{return_path_params}"
            yemot_commands.append(f"read=t-ברוך הבא למחשבון. אנא הקש מספר ראשון=digits,,,{return_path}")
        else: # אם בדרך כלל יש digits, נעבור לשלב הבא (כמו אם חוזרים מהשלב הקודם)
            return_path_params = urlencode({'step': '2', 'num1': digits})
            return_path = f"/?{return_path_params}"
            yemot_commands.append(f"go_to_folder={return_path}")
    
    # ------------------
    # שלב 2: קבלת הפעולה
    # ------------------
    elif step == "2":
        first_number = params.get("num1")
        
        if not digits: # אם לא קיבלנו פעולה
            prompt = "t-אנא בחר פעולה: 1 לחיבור, 2 לחיסור, 3 לכפל, 4 לחילוק"
            return_path_params = urlencode({'step': '3', 'num1': first_number})
            return_path = f"/?{return_path_params}"
            yemot_commands.append(f"read={prompt}=digits,,1,1,{return_path}")
        else: # קיבלנו פעולה
            operation = digits
            return_path_params = urlencode({'step': '3', 'num1': first_number, 'op': operation})
            return_path = f"/?{return_path_params}"
            yemot_commands.append(f"go_to_folder={return_path}")

    # ------------------
    # שלב 3: קבלת המספר השני
    # ------------------
    elif step == "3":
        operation = params.get("op")
        first_number = params.get("num1")
        
        if not digits: # אם לא קיבלנו את המספר השני
            prompt = "t-אנא הקש את המספר השני"
            return_path_params = urlencode({'step': '4', 'num1': first_number, 'op': operation})
            return_path = f"/?{return_path_params}"
            yemot_commands.append(f"read={prompt}=digits,,,{return_path}") # נבקש מספר שני, כל אורכו
        else:
            # קיבלנו את המספר השני, נעבור לשלב 4 לביצוע החישוב
            second_number_str = digits
            return_path_params = urlencode({'step': '4', 'num1': first_number, 'op': operation, 'num2': second_number_str})
            return_path = f"/?{return_path_params}"
            yemot_commands.append(f"go_to_folder={return_path}")

    # ------------------
    # שלב 4: ביצוע החישוב והצגת התוצאה
    # ------------------
    elif step == "4":
        operation = params.get("op")
        first_number_str = params.get("num1")
        second_number_str = params.get("num2")
        
        try:
            first_number = float(first_number_str)
            second_number = float(second_number_str)
            result_text = "שגיאה"

            if operation == "1": result_text = str(first_number + second_number)
            elif operation == "2": result_text = str(first_number - second_number)
            elif operation == "3": result_text = str(first_number * second_number)
            elif operation == "4":
                if second_number == 0:
                    result_text = "לא ניתן לחלק באפס"
                else:
                    result_text = str(round(first_number / second_number, 2))
            
            yemot_commands.append(f"id_list_message=t-התוצאה היא {result_text}")
            yemot_commands.append("go_to_folder=hangup")

        except ValueError:
            yemot_commands.append("id_list_message=t-אחד המספרים שהוקשו אינו תקין")
            yemot_commands.append("go_to_folder=hangup")
        except Exception as e:
            print(f"Error during calculation: {e}")
            yemot_commands.append("id_list_message=t-אירעה שגיאה כללית בחישוב")
            yemot_commands.append("go_to_folder=hangup")

    # אם הגענו לכאן בלי פקודות, ננתק
    if not yemot_commands:
        yemot_commands.append("go_to_folder=hangup")
        
    response_string = "&".join(yemot_commands)
    return Response(response_string, mimetype='text/plain; charset=UTF-8')
