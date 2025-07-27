# העתק את כל הקוד הזה והדבק אותו בקובץ a.py

from flask import Flask, request, Response
import os

# 1. הגדרת אפליקציית Flask
app = Flask(__name__)

# 2. הגדרת נתיב (route) שיקבל את כל הפניות מימות המשיח
@app.route('/yemot', methods=['POST', 'GET'])
def yemot_calculator():
    # רשימה לאיסוף כל הפקודות שנרצה לשלוח לימות המשיח
    yemot_commands = []

    # ב-Flask, הנתונים מגיעים או מ-form (בבקשת POST) או מ-args (בבקשת GET)
    # הקוד הזה בודק את שניהם כדי להיות בטוח
    params = request.form if request.form else request.args

    # קבלת המשתנים מהפנייה של ימות המשיח
    step = params.get("step", "1")
    digits = params.get("digits", "")
    callerid = params.get("ApiPhone", "") # השתמש במשתנה הרשמי של ימות המשיח
    path = params.get("path", "")
    
    # בדיקה שהתקבל מספר מתקשר כדי שנוכל ליצור קבצים
    if not callerid:
        # אם אין מספר מתקשר, אי אפשר להמשיך, נחזיר שגיאה
        yemot_commands.append("say=שגיאה. לא התקבל מספר מחייג")
        response_string = "&".join(yemot_commands)
        return Response(response_string, mimetype='text/plain')

    # הגדרת נתיבים לקבצים זמניים
    base = "/tmp/" + callerid + "_" + path.replace("/", "_")
    num1_file = base + "_num1.txt"
    operation_file = base + "_op.txt"
    
    # שלב 1 – קבלת מספר ראשון
    if step == "1":
        if not digits:
            yemot_commands.append("read=t-הקש את המספר הראשון=get_num1")
        else:
            with open(num1_file, "w") as f:
                f.write(digits)
            yemot_commands.append("read=t-בחר את הפעולה. 1 לחיבור, 2 לחיסור, 3 לכפל, 4 לחילוק=get_op,1,1")
        
        yemot_commands.append(f"go_to_folder=/yemot?step=2") # מעבר לשלב הבא

    # שלב 2 – קבלת פעולה
    elif step == "2":
        if not digits or digits not in ["1", "2", "3", "4"]:
            yemot_commands.append("read=t-בחירה שגויה. הקש 1 לחיבור, 2 לחיסור, 3 לכפל, 4 לחילוק=get_op,1,1")
            yemot_commands.append("go_to_folder=/yemot?step=2")
        else:
            with open(operation_file, "w") as f:
                f.write(digits)
            yemot_commands.append("read=t-הקש את המספר השני=get_num2")
            yemot_commands.append("go_to_folder=/yemot?step=3")

    # שלב 3 – קבלת מספר שני וחישוב
    elif step == "3":
        if not digits:
            yemot_commands.append("read=t-הקש את המספר השני=get_num2")
            yemot_commands.append("go_to_folder=/yemot?step=3")
        else:
            try:
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

            except ZeroDivisionError:
                yemot_commands.append("say=אי אפשר לחלק באפס")
            except Exception as e:
                print("General error:", e) # ידפיס שגיאה ללוג של Render
                yemot_commands.append("say=שגיאה כללית בחישוב")
            finally:
                # ניקוי הקבצים
                for f in [num1_file, operation_file]:
                    if os.path.exists(f): os.remove(f)

        yemot_commands.append("go_to_folder=hangup") # ניתוק בסיום

    # 3. איחוד כל הפקודות למחרוזת אחת והחזרתה כתשובת HTTP
    response_string = "&".join(yemot_commands)
    return Response(response_string, mimetype='text/plain')

# הערה: אין יותר צורך בקוד מחוץ לפונקציה, כמו if __name__ == '__main__' וכו'
# Gunicorn מפעיל ישירות את האובייקט app
