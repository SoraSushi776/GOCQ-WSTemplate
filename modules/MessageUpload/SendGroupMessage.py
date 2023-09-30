import json

from modules.Application.printc import printc


class SendGroupMessage:
    def __init__(self, group_id, message):
        self.group_id = group_id
        self.message = message

    def dump(self):
        printc("正在发送群聊消息", "I")
        printc(" - 消息内容：" + self.message, "I")
        printc(" - 发送到：" + str(self.group_id), "I")
        print()  # 空行

        self.message = "【小巫正】 \n" + self.message

        return json.dumps(
            {
                "action": "send_group_msg",
                "params": {"group_id": self.group_id, "message": self.message},
            }
        )
