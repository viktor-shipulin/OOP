import json
import os
from datetime import datetime, timedelta

class UserDB:
    def __init__(self, filename="users.json"):
        self.filename = filename
        if not os.path.exists("logs"):
            os.makedirs("logs")
            
        data = self._load_db()
        self.users = data.get("users", {})
        self.post_count = data.get("post_count", 0)
        self.blacklist = data.get("blacklist", {})

    def _load_db(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except:
                    return {"users": {}, "post_count": 0, "blacklist": {}}
        return {"users": {}, "post_count": 0, "blacklist": {}}

    def save(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump({
                "users": self.users, 
                "post_count": self.post_count,
                "blacklist": self.blacklist
            }, f, ensure_ascii=False, indent=4)

    def is_registered(self, user_id):
        return str(user_id) in self.users

    def register(self, user_id, nickname):
        self.users[str(user_id)] = nickname
        self.save()

    def get_next_post_number(self):
        self.post_count += 1
        self.save()
        return self.post_count

    def is_banned(self, user_id):
        user_id = str(user_id)
        if user_id not in self.blacklist:
            return False
        end_time_str = self.blacklist[user_id]
        if end_time_str == "forever":
            return "навсегда"
        try:
            end_time = datetime.fromisoformat(end_time_str)
            if datetime.now() > end_time:
                del self.blacklist[user_id]
                self.save()
                return False
            return end_time.strftime("%d.%m.%Y %H:%M")
        except:
            return "навсегда"

    def add_to_blacklist(self, user_id, duration_days=None):
        user_id = str(user_id)
        if duration_days is None:
            self.blacklist[user_id] = "forever"
        else:
            end_time = datetime.now() + timedelta(days=duration_days)
            self.blacklist[user_id] = end_time.isoformat()
        self.save()

    def remove_from_blacklist(self, user_id):
        user_id = str(user_id)
        if user_id in self.blacklist:
            del self.blacklist[user_id]
            self.save()
            return True
        return False

    def get_ban_list(self):
        result = []
        for uid, until in self.blacklist.items():
            nickname = self.users.get(uid, "Неизвестный")
            result.append(f"• {nickname} (ID: {uid}) - до {until}")
        return result

    def log_message(self, user_id, text):
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file = f"logs/{user_id}.txt"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{time_str}] {text}\n")