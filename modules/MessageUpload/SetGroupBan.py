import json

from modules.Application.printc import printc


class SetGroupBan:
    def __init__(self, group_id, user_id, duration):
        self.group_id = group_id
        self.user_id = user_id
        self.duration = duration

    def dump(self):
        printc("正在禁言用户", "I")
        printc(" - 用户：" + str(self.user_id), "I")
        printc(" - 群组：" + str(self.group_id), "I")
        printc(" - 时长：" + str(self.duration), "I")
        print()  # 空行

        return json.dumps(
            {
                "action": "set_group_ban",
                "params": {
                    "group_id": self.group_id,
                    "user_id": self.user_id,
                    "duration": self.duration,
                },
            }
        )
