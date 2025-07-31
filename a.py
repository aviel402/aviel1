# העתק את כל הקוד הזה, החלף את הקובץ הקיים שלך a.py

from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/yemot', methods=['POST', 'GET'])
def yemot_calculator_stateless():
    yemot_commands = []
    # params יכיל את כל הפרמטרים מה-URL ומה-POST/GET
    params = request.values

    # קבלת נתונים מהבקשה
    step = params.get("step", "1")
    digits = params.get("digits", "") # הקלט הנוכחי של המשתמש
    
    # שלב 1 – קבלת מספר ראשון
    if step == "1":
        if not digits:
            yemot_commands.append("read=t-הקש את המספר הראשון=digits")
        else:
            # שלב הבא: נעביר את המספר שהוקש (digits) כפרמטר ב-URL
            yemot_commands.append(f"go_to_folder=/yemot?step=2&num1={digits}")

    # שלב 2 – קבלת פעולה
    elif step == "2":
        num1 = params.get("num1") # קבלת המספר הראשון מה-URL
        if not digits or digits not in ["1", "2", "3", "4"]:
            yemot_commands.append(f"read=t-בחר את הפעולה. 1 לחיבור, 2 לחיסור, 3 לכפל, 4 לחילוק=digits,1,1")
        else:
            # שלב הבא: נעביר את num1 ואת הפעולה (digits) ב-URL
            yemot_commands.append(f"go_to_folder=/yemot?step=3&num1={num1}&op={digits}")

    # שלב 3 – קבלת מספר שני וחישוב
    elif step == "3":
        num1_str = params.get("num1")
        op = params.get("op")
        
        if not digits:
            yemot_commands.append("read=t-הקש את המספר השני=digits")
        else:
            try:
                # אין יותר צורך לבדוק אם קבצים קיימים
                num1 = float(num1_str)
                num2 = float(digits)
                result_text = "שגיאה"

                if op == "1": result_text = str(num1 + num2)
                elif op == "2": result_text = str(num1 - num2)
                elif op == "3": result_text = str(num1 * num2)
                elif op == "4":
                    if num2 == 0: raise ZeroDivisionError
                    result = round(num1 / num2, 2)
                    result_text = str(result)

                yemot_commands.append("id_list_message=t-התוצאה היא " + result_text)
                yemot_commands.append("go_to_folder=hangup")

            except ZeroDivisionError:
                yemot_commands.append("id_list_message=t-לא ניתן לחלק באפס")
                yemot_commands.append("go_to_folder=hangup")
            except Exception as e:
                print(f"General error in calculation: {e}") 
                yemot_commands.append("id_list_message=t-אירעה שגיאה כללית בחישוב")
                yemot_commands.append("go_to_folder=hangup")

    # הרכבת התגובה הסופית
    response_string = "&".join(yemot_commands)
    return Response(response_string, mimetype='text/plain; charset=UTF-8')
