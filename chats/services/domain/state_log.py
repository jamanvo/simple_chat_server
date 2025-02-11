from pymongo import MongoClient

client = MongoClient("mongodb", 27017)


class ChatLogService:
    def __init__(self):
        self.db = client["chat_logs"]

    def _add_state_log(self, data: dict, state_type: str, ts: float) -> None:
        collection = self.db["state"]
        collection.insert_one(
            {
                "user_id": data["user_id"],
                "room_id": data["room_id"],
                "state": state_type,
                "timestamp": ts,
            }
        )

    def add_join_log(self, user_id: int, room_id: int, now_ts: float) -> None:
        self._add_state_log({"user_id": user_id, "room_id": room_id}, "join", now_ts)

    def add_left_log(self, user_id: int, room_id: int, now_ts: float) -> None:
        self._add_state_log({"user_id": user_id, "room_id": room_id}, "left", now_ts)
