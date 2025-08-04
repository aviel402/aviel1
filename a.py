# גרסה סופית ומתוקנת המשתמשת בכוכבית (*) כמפריד

from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/yemot', methods=['POST', 'GET'])
def yemot_single_input_calculator_star():
    yemot_commands = []
    params = request.values
    digits = params.get("digits", "")

    # אם המשתמש עוד לא הקיש כלום, נבקש ממנו את כל הקלט
    if not digits:
        # שינוי: החלפנו "סולמית" ב"כוכבית" בהנחיה למשתמש
        prompt = "t-לחישוב, הקש מספר ראשון, כוכבית, פעולת חשבון, כוכבית, מספר שני, וכוכבית לסיום"
        yemot_commands.append(f"read={prompt}=digits")
    
    # אם קיבלנו קלט, ננסה לחשב אותו
    else:
        try:
            # שינוי: נפרק את הקלט לפי כוכבית (*) במקום סולמית
            parts = digits.split('*')
            
            if len(parts) != 3:
                raise ValueError("קלט לא תקין")

            num1_str, op_str, num2_str = parts
            
            if op_str not in ['1', '2', '3', '4']:
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
            
            yemot_commands.append("id_list_message=t-התוצאה היא " + result_text)

        except Exception as e:
            print(f"Error processing input '{digits}': {e}")
            yemot_commands.append("id_list_message=t-הקלט שהוקש אינו תקין, אנא נסה שנית")
        finally:
            yemot_commands.append("go_to_folder=hangup")

    response_string = "&".join(yemot_commands)
    return Response(response_string, mimetype='text/plain; charset=UTF-8')
