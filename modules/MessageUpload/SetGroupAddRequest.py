import json

from modules.Application.Printc import Printc


class SetGroupAddRequest:
    def __init__(self, flag, sub_type, approve, reason):
        self.flag = flag
        self.sub_type = sub_type
        self.approve = approve
        self.reason = reason

    def dump(self):
        Printc("正在处理加群请求", "I")
        Printc(" - 消息内容：" + self.message, "I")
        Printc(" - 发送到：" + str(self.group_id), "I")
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
