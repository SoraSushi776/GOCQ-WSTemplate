import json

from modules.Application.printc import printc


class SetGroupAddRequest:
    def __init__(self, flag, sub_type, approve, reason):
        self.flag = flag
        self.sub_type = sub_type
        self.approve = approve
        self.reason = reason

    def dump(self):
        printc("正在处理加群请求", "I")
        printc(" - 消息内容：" + self.message, "I")
        printc(" - 发送到：" + str(self.group_id), "I")
        print()  # 空行

        return json.dumps(
            {
                "action": "_send_group_notice",
                "params": {
                    "flag": self.flag,
                    "sub_type": self.sub_type,
                    "approve": self.approve,
                    "reason": self.reason,
                },
            }
        )
