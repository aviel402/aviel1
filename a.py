# גרסה סופית ויציבה - מפרקת את ההודעה לחלקים כדי למנוע ניתוק אוטומטי

from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/yemot', methods=['POST', 'GET'])
def yemot_single_input_calculator_stable():
    yemot_commands = []
    params = request.values
    digits = params.get("digits", "")

    if not digits:
        # === שוברים את ההודעה הארוכה לכמה הודעות קצרות ===
        prompt1 = "t-שלום וברוך הבא למחשבון"
        prompt2 = "t-לחישוב, הקש מספר ראשון, כוכבית, פעולה, כוכבית, ומספר שני"
        prompt3 = "t-הפעולות הן: 1 לחיבור, 2 חיסור, 3 כפל, 4 חילוק, 5 חזקה"
        prompt4 = "t-בסיום, הקש כוכבית"

        # מוסיפים את כל ההודעות לרשימת הפקודות
        yemot_commands.append(f"id_list_message={prompt1}")
        yemot_commands.append(f"id_list_message={prompt2}")
        yemot_commands.append(f"id_list_message={prompt3}")
        yemot_commands.append(f"id_list_message={prompt4}")

        # אחרי שהשמענו הכל, עכשיו נבקש קלט
        # הפקודה read ריקה מהודעה כי כבר השמענו אותה
        yemot_commands.append("read==digits")
    else:
        try:
            parts = digits.split('*')
            
            if len(parts) != 3:
                raise ValueError("קלט לא תקין")

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
            yemot_commands.append("id_list_message=t-הקלט שהוקש אינו תקין, אנא נסה שנית")
        finally:
            yemot_commands.append("go_to_folder=hangup")

    response_string = "&".join(yemot_commands)
    return Response(response_string, mimetype='text/plain; charset=UTF-8')
