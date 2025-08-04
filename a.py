# החלף את כל הקוד שלך בגרסה הפשוטה והנכונה הזו

from flask import Flask, request, Response
from urllib.parse import urlencode

app = Flask(__name__)

@app.route('/yemot', methods=['POST', 'GET'])
def yemot_calculator_simple_and_correct():
    yemot_commands = []
    params = request.values

    step = params.get("step", "1")
    digits = params.get("digits", "")
    
    # שלב 1 – קבלת מספר ראשון
    if step == "1":
        if not digits:
            # פקודה פשוטה ונקייה: הודעה, שם משתנה, סוג=מספרים, מינימום=1, מקסימום=10
            # המערכת תשתמש בזמן ברירת המחדל שלה להמתנה (בדרך כלל 3-5 שניות)
            yemot_commands.append("read=t-הקש את המספר הראשון וסולמית לסיום=digits,yes,1,10")
        else:
            yemot_commands.append(f"go_to_folder=/yemot?step=2&num1={digits}")

    # שלב 2 – קבלת פעולה
    elif step == "2":
        num1 = params.get("num1")
        if not digits or digits not in ["1", "2", "3", "4"]:
            next_url_params = urlencode({'step': '2', 'num1': num1})
            next_url = f"/yemot?{next_url_params}"
            # פקודה זו נכונה: מינימום 1 ומקסימום 1, כדי לקלוט רק ספרה אחת
            yemot_commands.append(f"read=t-בחר את הפעולה=digits,yes,1,1,{next_url}")
        else:
            op = digits
            yemot_commands.append(f"go_to_folder=/yemot?step=3&num1={num1}&op={op}")

    # שלב 3 – קבלת מספר שני וחישוב
    elif step == "3":
        num1 = params.get("num1")
        op = params.get("op")
        
        if not digits:
            next_url_params = urlencode({'step': '3', 'num1': num1, 'op': op})
            next_url = f"/yemot?{next_url_params}"
            # אותה פקודה פשוטה כמו בשלב הראשון
            yemot_commands.append(f"read=t-הקש את המספר השני וסולמית לסיום=digits,yes,1,10,{next_url}")
        else:
            try:
                num2 = float(digits)
                num1_float = float(num1)
                result_text = "שגיאה"
                
                if op == "1": result_text = str(num1_float + num2)
                elif op == "2": result_text = str(num1_float - num2)
                elif op == "3": result_text = str(num1_float * num2)
                elif op == "4":
                    if num2 == 0: raise ZeroDivisionError
                    result = round(num1_float / num2, 2)
                    result_text = str(result)

                yemot_commands.append("id_list_message=t-התוצאה היא " + result_text)
                yemot_commands.append("go_to_folder=hangup")

            except Exception as e:
                print(f"ERROR: {e}, PARAMS: {params}") 
                yemot_commands.append("id_list_message=t-אירעה שגיאה בחישוב")
                yemot_commands.append("go_to_folder=hangup")

    response_string = "&".join(yemot_commands)
    return Response(response_string, mimetype='text/plain; charset=UTF-8')
