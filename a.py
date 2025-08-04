# גרסה חדשה של הראוטר, בנויה מחדש על בסיס הקוד היציב

from flask import Flask, request, Response
import datetime

app = Flask(__name__)

# --- אפליקציה מס' 1: המחשבון (מהגרסה האחרונה שעבדה) ---
def handle_calculator(params):
    yemot_commands = []
    digits = params.get("digits", "")

    main_prompt = "t-לחישוב, הקש מספר, כוכבית, פעולה, כוכבית, ומספר. לעזרה, הקש כוכבית."
    help_prompt = "t-הפעולות הן: 1 חיבור, 2 חיסור, 3 כפל, 4 חילוק, 5 חזקה."

    if not digits:
        yemot_commands.append(f"read={main_prompt}=digits")
    elif digits == '*':
        yemot_commands.append(f"id_list_message={help_prompt}")
        yemot_commands.append(f"read={main_prompt}=digits")
    else:
        try:
            parts = digits.split('*')
            if len(parts) != 3: raise ValueError("קלט לא תקין")
            num1_str, op_str, num2_str = parts
            if op_str not in ['1', '2', '3', '4', '5']: raise ValueError("פעולה לא תקינה")
            
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
                    result_text = str(round(num1 / num2, 2))
            elif op_str == "5": result_text = str(num1 ** num2)
            
            yemot_commands.append("id_list_message=t-התוצאה היא " + result_text)
        except Exception:
            yemot_commands.append("id_list_message=t-הקלט שהוקש אינו תקין")
        finally:
            yemot_commands.append("go_to_folder=hangup")
            
    return yemot_commands

# --- אפליקציה מס' 2: השעון ---
def handle_time(params):
    yemot_commands = []
    
    # אזור זמן ישראל (UTC+3 בקיץ)
    tz = datetime.timezone(datetime.timedelta(hours=3))
    now = datetime.datetime.now(tz)
    hour = now.hour
    minute = now.minute
    
    time_str = f"t-השעה כעת היא {hour} ו {minute} דקות"
    
    yemot_commands.append(f"id_list_message={time_str}")
    yemot_commands.append("go_to_folder=hangup")
    
    return yemot_commands

# --- הנתב הראשי ---
@app.route('/yemot-router', methods=['POST', 'GET'])
def yemot_router():
    try:
        params = request.values
        extension = params.get("ApiExtension", "")
        
        yemot_commands = []

        if extension == '1':
            yemot_commands = handle_calculator(params)
        elif extension == '2':
            yemot_commands = handle_time(params)
        else:
            # אם התקשרו משלוחה לא מוכרת
            yemot_commands.append("id_list_message=t-שלוחה זו אינה מוגדרת במערכת")
            yemot_commands.append("go_to_folder=hangup")

    except Exception as e:
        # רשת ביטחון: אם משהו קורס, נדפיס את השגיאה ללוג ונשמיע הודעה
        print(f"FATAL ERROR IN ROUTER: {e}")
        yemot_commands = [
            "id_list_message=t-אירעה שגיאה כללית בשרת, אנא נסה שנית במועד מאוחר יותר",
            "go_to_folder=hangup"
        ]

    # הרכבת התגובה הסופית ושליחתה
    response_string = "&".join(yemot_commands)
    return Response(response_string, mimetype='text/plain; charset=UTF-8')
