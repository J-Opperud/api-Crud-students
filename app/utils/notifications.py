from datetime import datetime
import time



def log_activity(user_id: int, action: str,):
    """Creates a log for a new user"""
    timestap = datetime.now().isoformat()
    time_delay = time.sleep(2)

    with open(
        "activity_log.txt", "a") as file:
        file.write(
            f"{time_delay}{timestap} | User {user_id} {action}\n"
            )

def send_notification(email: str, message: str):
    """Creates and sends a notification"""
    time_delay = time.sleep(2)
    timestamp = datetime.now().isoformat()

    with open(
        "notification_log.txt","a") as file:
        file.write(
            f"{time_delay} |{timestamp} | email: {email}  {message}" 
            )





