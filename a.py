# העתק את כל הקוד הזה והדבק אותו בקובץ a.py

from flask import Flask, request, Response
import os

app = Flask(__name__)

@app.route('/yemot', methods=['POST', 'GET'])
def yemot_calculator():
    yemot_commands = []
    params = request.form if request.form else request.args

    # קבלת משתנים - שימו לב, אנחנו תמיד קוראים לנתונים שהתקבלו "digits"
    step = params.get("step", "1")
    digits = params.get("digits", "") # כאן אנו מקבלים את קלט המשתמש
    callerid = params.get("ApiPhone", "") 
    path = params.get("path", "")
    
    if not callerid:
        yemot_commands.append("say=שגיאה. לא התקבל מספר מחייג")
        return Response("&".join(yemot_commands), mimetype='text/plain')

    base = "/tmp/" + callerid + "_" + path.replace("/", "_")
    num1_file = base + "_num1.txt"
    operation_file = base + "_op.txt"
    
    # שלב 1 – קבלת מספר ראשון
    if step == "1":
        if not digits:
            # תיקון: אנו מבקשים מימות להחזיר את הקלט תחת השם "digits"
            yemot_commands.append("read=t-הקש את המספר הראשון=digits")
        else:
            with open(num1_file, "w") as f:
                f.write(digits)
            yemot_commands.append(f"go_to_folder=/yemot?step=2")

    # שלב 2 – קבלת פעולה
    elif step == "2":
        if not digits or digits not in ["1", "2", "3", "4"]:
             # תיקון: אנו מבקשים מימות להחזיר את הקלט תחת השם "digits"
            yemot_commands.append("read=t-בחר את הפעולה. 1 לחיבור, 2 לחיסור, 3 לכפל, 4 לחילוק=digits,1,1")
        else:
            with open(operation_file, "w") as f:
                f.write(digits)
            yemot_commands.append("go_to_folder=/yemot?step=3")

    # שלב 3 – קבלת מספר שני וחישוב
    elif step == "3":
        if not digits:
             # תיקון: אנו מבקשים מימות להחזיר את הקלט תחת השם "digits"
            yemot_commands.append("read=t-הקש את המספר השני=digits")
        else:
            try:
                if not os.path.exists(num1_file) or not os.path.exists(operation_file):
                    # הגנה במקרה שהקבצים נמחקו או לא נוצרו
                    yemot_commands.append("say=שגיאה במערכת, אנא נסה שנית")
                    yemot_commands.append("go_to_folder=/yemot") # חזרה להתחלה
                else:
                    num1 = float(open(num1_file).read())
                    op = open(operation_file).read().strip()
                    num2 = float(digits)
                    result_text = "שגיאה"

                    if op == "1": result_text = str(num1 + num2)
                    elif op == "2": result_text = str(num1 - num2)
                    elif op == "3": result_text = str(num1 * num2)
                    elif op == "4":
                        if num2 == 0: raise ZeroDivisionError
                        result_text = str(num1 / num2)

                    yemot_commands.append("say=התוצאה היא " + result_text)
                    yemot_commands.append("go_to_folder=hangup") # ניתוק בסיום

            except ZeroDivisionError:
                yemot_commands.append("say=אי אפשר לחלק באפס")
                yemot_commands.append("go_to_folder=hangup")
            except Exception as e:
                print(f"General error in calculation: {e}") 
                yemot_commands.append("say=שגיאה כללית בחישוב")
                yemot_commands.append("go_to_folder=hangup")
            finally:
                # ניקוי הקבצים
                for f in [num1_file, operation_file]:
                    if os.path.exists(f): os.remove(f)
                    
    # בניית התגובה הסופית
    response_string = "&".join(yemot_commands)
    return Response(response_string, mimetype='text/plain')
