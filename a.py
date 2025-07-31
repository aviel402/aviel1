# קוד מתוקן סופית - עם שמירת פרמטרים בפקודת ה-read

from flask import Flask, request, Response
from urllib.parse import urlencode

app = Flask(__name__)

@app.route('/yemot', methods=['POST', 'GET'])
def yemot_calculator_stateless():
    yemot_commands = []
    params = request.values

    step = params.get("step", "1")
    digits = params.get("digits", "")
    
    # שלב 1 – קבלת מספר ראשון
    if step == "1":
        if not digits:
            # ה-read הראשון תמיד חוזר לכתובת הראשית, וזה בסדר
            yemot_commands.append("read=t-הקש את המספר הראשון=digits,no,1,10,hangup")
        else:
            yemot_commands.append(f"go_to_folder=/yemot?step=2&num1={digits}")

    # שלב 2 – קבלת פעולה
    elif step == "2":
        num1 = params.get("num1")
        if not digits or digits not in ["1", "2", "3", "4"]:
            # **** תיקון קריטי ****
            # נבנה את הכתובת שה-read יחזור אליה
            next_url_params = urlencode({'step': '2', 'num1': num1})
            next_url = f"/yemot?{next_url_params}"
            
            # ה-read יחזור לכתובת המדויקת, כולל המידע על num1
            yemot_commands.append(f"read=t-בחר את הפעולה. 1 לחיבור, 2 לחיסור, 3 לכפל, 4 לחילוק=digits,no,1,1,hangup,{next_url}")
        else:
            op = digits
            yemot_commands.append(f"go_to_folder=/yemot?step=3&num1={num1}&op={op}")

    # שלב 3 – קבלת מספר שני וחישוב
    elif step == "3":
        num1 = params.get("num1")
        op = params.get("op")
        
        if not digits:
            # **** תיקון קריטי ****
            # נבנה את הכתובת שה-read יחזור אליה
            next_url_params = urlencode({'step': '3', 'num1': num1, 'op': op})
            next_url = f"/yemot?{next_url_params}"

            # ה-read יחזור לכתובת המדויקת, כולל המידע על num1 ו-op
            yemot_commands.append(f"read=t-הקש את המספר השני=digits,no,1,10,hangup,{next_url}")
        else:
            try:
                num2 = float(digits)
                result_text = "שגיאה"
                
                if op == "1": result_text = str(float(num1) + num2)
                elif op == "2": result_text = str(float(num1) - num2)
                elif op == "3": result_text = str(float(num1) * num2)
                elif op == "4":
                    if num2 == 0: raise ZeroDivisionError
                    result = round(float(num1) / num2, 2)
                    result_text = str(result)

                yemot_commands.append("id_list_message=t-התוצאה היא " + result_text)
                yemot_commands.append("go_to_folder=hangup")

            except ZeroDivisionError:
                yemot_commands.append("id_list_message=t-לא ניתן לחלק באפס")
                yemot_commands.append("go_to_folder=hangup")
            except Exception as e:
                print(f"ERROR: {e}, PARAMS: {params}") 
                yemot_commands.append("id_list_message=t-אירעה שגיאה כללית בחישוב")
                yemot_commands.append("go_to_folder=hangup")

    response_string = "&".join(yemot_commands)
    return Response(response_string, mimetype='text/plain; charset=UTF-8')
