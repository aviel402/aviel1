# קוד: api/index.py (עם שילוב משחק התפקידים בשלוחה 5)

from flask import Flask, request, Response
import datetime
import random

app = Flask(__name__)

# =======================================================
#               הגדרות וקלאסים של המשחק
# =======================================================

# זהו "מסד הנתונים" הזמני שלנו. במערכת אמיתית, זה יוחלף בחיבור ל-DB.
game_data_db = {}

class דמות:
    # ... (כל הקוד של הקלאס 'דמות' שלך, ללא שינוי) ...
    def __init__(self, שם, בריאות, התקפה):
        self.שם = שם
        self.בריאות = בריאות
        self.התקפה = התקפה
        self.זהב = 0
        self.כוח = 0

class מפלצת_פנטזיה:
    # ... (כל הקוד של הקלאס 'מפלצת_פנטזיה' שלך, ללא שינוי) ...
    def __init__(self, שם, בריאות, התקפה):
        self.שם = שם
        self.בריאות = בריאות
        self.התקפה = התקפה

def יצירת_מפלצות(כוח):
    # ... (כל הקוד של הפונקציה 'יצירת_מפלצות' שלך, ללא שינוי) ...
    מפלצות = []
    # ... (כל רשימת המפלצות) ...
    return מפלצות

# =======================================================
#       פונקציות עזר לטעינה ושמירה של דמות השחקן
# =======================================================

def load_player_data(caller_id):
    """ טוען נתוני שחקן מה'בסיס נתונים'. אם לא קיים, יוצר דמות חדשה. """
    if caller_id not in game_data_db:
        # שחקן חדש - ניצור לו דמות התחלתית
        game_data_db[caller_id] = {
            'health': 100,
            'attack': 20,
            'gold': 0,
            'power': 0,
            'current_monster': None # שדה שיחזיק את המפלצת הנוכחית בקרב
        }
    return game_data_db[caller_id]

def save_player_data(caller_id, data):
    """ שומר את נתוני השחקן המעודכנים. """
    game_data_db[caller_id] = data


# =======================================================
#               הפונקציה הראשית של המשחק
# =======================================================

def handle_custom_game(params):
    yemot_commands = []
    caller_id = params.get("ApiPhone", "default_player") # מזהה ייחודי לשחקן
    if not caller_id:
        return ["id_list_message=t-לא זוהה מספר טלפון. לא ניתן לשמור את המשחק."]

    # טעינת "קובץ השמירה" של השחקן
    player_data = load_player_data(caller_id)
    
    # בדיקת קלט המשתמש ו"מצב" המשחק
    digits = params.get("digits", "")
    game_step = params.get("game_step", "main_menu") # קובע באיזה "סצנה" אנחנו

    # --- סצנה 1: התפריט הראשי ---
    if game_step == "main_menu":
        prompt = (f"t-שלום לך. יש לך {player_data['health']} חיים ו-{player_data['gold']} זהב. "
                  f"להילחם הקש 1. לחנות הקש 2.")
        return_path = f"/?ApiExtension=5&game_step=menu_choice" # לאן לחזור אחרי הבחירה
        yemot_commands.append(f"read={prompt}=digits,,1,1,{return_path}")

    # --- עיבוד הבחירה מהתפריט הראשי ---
    elif game_step == "menu_choice":
        if digits == "1": # בחר להילחם
            monsters_list = יצירת_מפלצות(player_data['power'])
            if not monsters_list:
                 yemot_commands.append("id_list_message=t-ניצחת את כל המפלצות. כל הכבוד.")
            else:
                monster_obj = random.choice(monsters_list)
                # שומרים את נתוני המפלצת ב"קובץ השמירה" כדי לזכור אותה בסיבוב הבא
                player_data['current_monster'] = {
                    'name': monster_obj.שם,
                    'health': monster_obj.בריאות,
                    'attack': monster_obj.התקפה
                }
                save_player_data(caller_id, player_data)
                
                prompt = f"t-יצאת להילחם ופגשת {monster_obj.שם} עם {monster_obj.בריאות} חיים. לתקוף הקש 1, לברוח הקש 2."
                return_path = f"/?ApiExtension=5&game_step=combat_action"
                yemot_commands.append(f"read={prompt}=digits,,1,1,{return_path}")

        elif digits == "2": # בחר ללכת לחנות
             prompt = f"t-ברוך הבא לחנות. יש לך {player_data['gold']} זהב. לקניית 10 חיים ב-10 זהב הקש 1. לקניית 5 התקפה ב-15 זהב הקש 2. לחזרה הקש 3."
             return_path = f"/?ApiExtension=5&game_step=shop_action"
             yemot_commands.append(f"read={prompt}=digits,,1,1,{return_path}")

    # --- סצנה 2: פעולת קרב ---
    elif game_step == "combat_action":
        monster_data = player_data.get('current_monster')
        if not monster_data: # הגנה למקרה שהגענו לכאן בטעות
            return ["id_list_message=t-שגיאה, לא נמצאה מפלצת להילחם בה.", "go_to_folder=/?ApiExtension=5&game_step=main_menu"]

        # לוגיקת הקרב
        if digits == "1": # השחקן תוקף
            monster_data['health'] -= player_data['attack']
            
            if monster_data['health'] <= 0: # המפלצת מתה
                loot = random.randint(10, 50)
                player_data['gold'] += loot
                player_data['current_monster'] = None
                save_player_data(caller_id, player_data)
                yemot_commands.append(f"id_list_message=t-ניצחת את ה{monster_data['name']} וקיבלת {loot} זהב.")
                yemot_commands.append("go_to_folder=/?ApiExtension=5&game_step=main_menu")

            else: # המפלצת עדיין חיה ותוקפת בחזרה
                player_data['health'] -= monster_data['attack']
                
                if player_data['health'] <= 0: # השחקן מת
                    yemot_commands.append(f"id_list_message=t-ה{monster_data['name']} ניצח אותך. המשחק נגמר.")
                    # אפשר לאפס את השחקן או פשוט לנתק
                    game_data_db.pop(caller_id, None) # מחיקת השמירה
                else: # הקרב ממשיך
                    save_player_data(caller_id, player_data)
                    prompt = f"t-תקפת! ל{monster_data['name']} נותרו {monster_data['health']} חיים. הוא תקף בחזרה, ונותרו לך {player_data['health']} חיים. לתקוף שוב הקש 1, לברוח הקש 2."
                    return_path = f"/?ApiExtension=5&game_step=combat_action"
                    yemot_commands.append(f"read={prompt}=digits,,1,1,{return_path}")

        elif digits == "2": # השחקן בורח
            player_data['current_monster'] = None
            save_player_data(caller_id, player_data)
            yemot_commands.append("id_list_message=t-ברחת מהקרב.")
            yemot_commands.append("go_to_folder=/?ApiExtension=5&game_step=main_menu")

    # --- סצנה 3: פעולה בחנות ---
    elif game_step == "shop_action":
        if digits == "1": # קנה חיים
            if player_data['gold'] >= 10:
                player_data['health'] += 10
                player_data['gold'] -= 10
                yemot_commands.append("id_list_message=t-קנית 10 חיים.")
            else:
                yemot_commands.append("id_list_message=t-אין לך מספיק זהב.")
        elif digits == "2": # קנה התקפה
             if player_data['gold'] >= 15:
                player_data['attack'] += 5
                player_data['power'] += 5
                player_data['gold'] -= 15
                yemot_commands.append("id_list_message=t-קנית 5 התקפה.")
             else:
                yemot_commands.append("id_list_message=t-אין לך מספיק זהב.")
        
        save_player_data(caller_id, player_data)
        yemot_commands.append("go_to_folder=/?ApiExtension=5&game_step=main_menu")

    return yemot_commands


# ... (וכאן ממשיך שאר הקוד של הראוטר הראשי, שקורא לפונקציה הזו כשהשלוחה היא 5)
