# גרסה סופית ושימושית - כולל הסבר על פעולות החשבון

from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/yemot', methods=['POST', 'GET'])
def yemot_single_input_calculator_star():
    yemot_commands = []
    params = request.values
    digits = params.get("digits", "")

    # אם המשתמש עוד לא הקיש כלום, נבקש ממנו את כל הקלט
    if not digits:
        # **** השינוי החשוב נמצא כאן! ****
        # הוספנו את ההסבר על הפעולות להודעת הפתיחה
        prompt = "t-שלום הגעת למחשבון,לחישוב, הקש מספר ראשון, כוכבית, פעולה, כוכבית, מספר שני, וכוכבית לסיום. לפעולות החשבון, הקש 1 לחיבור, 2 לחיסור, 3 לכפל, 4 לחילוק או 5 לחזקה ."
        yemot_commands.append(f"read={prompt}=digits")
    
    # אם קיבלנו קלט, ננסה לחשב אותו
    else:
        try:
            parts = digits.split('*')
            
            if len(parts) != 3:
                raise ValueError("קלט לא תקין")

            num1_str, op_str, num2_str = parts
            
            if op_str not in ['1', '2', '3', '4','5']:
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
            elif op_str == "5":esult_text = str(num1 ** num2)

            yemot_commands.append("id_list_message=t-התוצאה היא " + result_text)

        except Exception as e:
            print(f"Error processing input '{digits}': {e}")
            yemot_commands.append("id_list_message=t-הקלט שהוקש אינו תקין, אנא נסה שנית")
        finally:
            yemot_commands.append("go_to_folder=hangup")

    response_string = "&".join(yemot_commands)
    return Response(response_string, mimetype='text/plain; charset=UTF-8')
