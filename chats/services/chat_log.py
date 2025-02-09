import copy

from pymongo import MongoClient

client = MongoClient("mongodb", 27017)


class ChatLogService:
    def __init__(self):
        self.db = client["chat_logs"]

    def add_state_log(self, data: dict, state_type: str, ts: float) -> None:
        collection = self.db["state"]
        collection.insert_one(
            {
                "user_id": data["user_id"],
                "room_id": data["room_id"],
                "state": state_type,
                "timestamp": ts,
            }
        )

    async def add_message(self, data: dict, ts: float) -> None:
        insert_data = copy.deepcopy(data)
        insert_data["timestamp"] = ts
        result = self.db["messages"].insert_one(insert_data)

        self.db["room_messages"].update_one(
            {"_id": f"chatroom_{insert_data['room_id']}"},
            {"$push": {"message_ids": str(result.inserted_id)}},
        )
