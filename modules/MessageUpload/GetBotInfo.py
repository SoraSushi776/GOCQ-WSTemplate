import json

from modules.Application.printc import printc


class GetBotInfo:
    printc("正在获取机器人信息", "I")
    print()  # 空行

    def dump(self):
        return json.dumps(
            {
                "action": "get_login_info",
            }
        )
