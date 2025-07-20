import requests

# הגדרת כתובת ה-API
url = "https://www.call2all.co.il/ym/api/GetIncomingCalls?token=0747954855:112233"

# שליחת הבקשה
response = requests.get(url)

# בדיקת סטטוס
if response.status_code == 200:
    data = response.json()
    text = data.get('callsCount', 0)
    print(f"id_list_message=t-כרגע יש במערכת.n-{text}.t-מאזינים.")
else:
    print("שגיאה בבקשת הנתונים:", response.status_code)
