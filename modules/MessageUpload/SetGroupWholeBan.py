import json

from modules.Application.printc import printc


class SetGroupWholeBan:
    def __init__(self, group_id, enable):
        self.group_id = 0
        self.enable = False

    def dump(self):
        printc("正在设置全体禁言", "I")
        printc(" - 群组：" + str(self.group_id), "I")
        printc(" - 是否开启：" + str(self.enable), "I")
        print()  # 空行

        return json.dumps(
            {
                "action": "set_group_whole_ban",
                "params": {"group_id": self.group_id, "enable": self.enable},
            }
        )
