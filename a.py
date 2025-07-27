from flask import request
print("Content-Type: text/plain\n")

# משתנים מה-URL
step = request.args.get("step", "1")  # שלב
digits = request.args.get("digits", "")
callerid = request.args.get("callerid", "")
path = request.args.get("path", "")

# קבצים לשמירה זמנית של הקלטים (בתיקיית tmp)
import os
base = "/tmp/" + callerid + "_" + path.replace("/", "_")
num1_file = base + "_num1.txt"
operation_file = base + "_op.txt"

# שלב 1 – קבלת מספר ראשון
if step == "1":
    if not digits:
        print("say=הקש את המספר הראשון")
        print("record_digits=yes")
        print("goto=A.py?step=1")  # חזרה לאותו שלב עם קלט
    else:
        with open(num1_file, "w") as f:
            f.write(digits)
        print("say=בחר את הפעולה. הקש 1 לחיבור, 2 לחיסור, 3 לכפל, 4 לחילוק")
        print("record_digits=yes\nmax_digits=1")
        print("goto=A.py?step=2")

# שלב 2 – קבלת פעולה
elif step == "2":
    if not digits or digits not in ["1", "2", "3", "4"]:
        print("say=בחירה לא תקינה. הקש 1 לחיבור, 2 לחיסור, 3 לכפל, 4 לחילוק")
        print("record_digits=yes\nmax_digits=1")
        print("goto=A.py?step=2")
    else:
        with open(operation_file, "w") as f:
            f.write(digits)
        print("say=הקש את המספר השני")
        print("record_digits=yes")
        print("goto=A.py?step=3")

# שלב 3 – קבלת מספר שני וחישוב
elif step == "3":
    if not digits:
        print("say=הקש את המספר השני")
        print("record_digits=yes")
        print("goto=A.py?step=3")
    else:
        try:
            num1 = float(open(num1_file).read())
            op = open(operation_file).read().strip()
            num2 = float(digits)

            if op == "1":
                result = num1 + num2
            elif op == "2":
                result = num1 - num2
            elif op == "3":
                result = num1 * num2
            elif op == "4":
                if num2 == 0:
                    raise ZeroDivisionError
                result = num1 / num2
            else:
                result = "שגיאה"

            # השמעת התוצאה
            print(f"say=התוצאה היא {result}")

        except ZeroDivisionError:
            print("say=אי אפשר לחלק באפס")
        except:
            print("say=שגיאה כללית בחישוב")

        # ניקוי הקבצים
        for f in [num1_file, operation_file]:
            try:
                os.remove(f)
            except:
                pass

        print("goto=menu/0")
