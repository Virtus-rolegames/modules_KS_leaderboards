async def send_message(user_id, text: str, ):
    print(f"sent: '{text}', to user {user_id}")


class User:
    def __init__(self, user_id, username: str | None = None, win_points: int = 0):
        self.user_id = user_id
        self.win_points = win_points
        self.username = username if username else str(user_id)
