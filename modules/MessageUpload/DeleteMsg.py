import json

from modules.Application.printc import printc


class DeleteMsg:
    def __init__(self, message_id):
        self.message_id = message_id

    def dump(self):
        printc("正在撤回消息", "I")
        printc(" - 消息ID：" + str(self.message_id), "I")
        print()  # 空行

        return json.dumps(
            {
                "action": "delete_msg",
                "params": {"message_id": self.message_id},
            }
        )
