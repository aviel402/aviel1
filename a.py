# גרסה חדשה ומשופרת עם תפריט עזרה ייעודי לכוכבית

from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/yemot', methods=['POST', 'GET'])
def yemot_calculator_with_help():
    yemot_commands = []
    params = request.values
    digits = params.get("digits", "")

    # הגדרת ההודעות במקום אחד כדי שיהיה קל לערוך
    main_prompt = "t-לחישוב, הקש מספר, כוכבית, פעולה, כוכבית, ומספר. לשמיעת רשימת הפעולות, הקש כוכבית."
    help_prompt = "t-הפעולות הן: 1 לחיבור, 2 לחיסור, 3 לכפל, 4 לחילוק, או 5 לחזקה."

    # --- הלוגיקה הראשית ---

    # אם המשתמש עוד לא הקיש כלום (שיחה חדשה)
    if not digits:
        yemot_commands.append(f"read={main_prompt}=digits")
    
    # אם המשתמש ביקש עזרה
    elif digits == '*':
        yemot_commands.append(f"id_list_message={help_prompt}")
        # אחרי העזרה, נחזור להודעה הראשית ונמתין לקלט
        yemot_commands.append(f"read={main_prompt}=digits")

    # אם המשתמש הקיש תרגיל לחישוב
    else:
        try:
            parts = digits.split('*')
            
            if len(parts) != 3:
                raise ValueError("קלט לא תקין, חייבים שני תווי כוכבית")

            num1_str, op_str, num2_str = parts
            
            if op_str not in ['1', '2', '3', '4', '5']:
                raise ValueError("פעולת חשבון לא תקינה")

            num1 = float(num1_str)
            num2 = float(num2_str)
            result_text = "שגיאה"

            if op_str == "1": result_text = str(num1 + num2)
            elif op_str == "2": result_text = str(num1 - num2)
            elif op_str == "3": result_text = str(num1 * num2)
            elif op_str == "4":
                if num2 == 0:
                    result_text = "לא ניתן לחלק באפס"
                else:
                    result = round(num1 / num2, 2)
                    result_text = str(result)
            elif op_str == "5": result_text = str(num1 ** num2)

            yemot_commands.append("id_list_message=t-התוצאה היא " + result_text)

        except Exception as e:
            print(f"Error processing input '{digits}': {e}")
            yemot_commands.append("id_list_message=t-הקלט שהוקש אינו תקין")
        finally:
            yemot_commands.append("go_to_folder=hangup")

    response_string = "&".join(yemot_commands)
    return Response(response_string, mimetype='text/plain; charset=UTF-8')
