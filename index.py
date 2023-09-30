# 导入模块
import os
import sys
import websockets
import asyncio
import datetime
import time
import json
import traceback
import re
import requests

# 导入自定义模块
from modules.Application.printc import printc

# 导入指令模块
from modules.BotModules.Template import Template

# 导入上报消息模块
from modules.MessageUpload.SendPrivateMessage import SendPrivateMessage
from modules.MessageUpload.SendGroupMessage import SendGroupMessage
from modules.MessageUpload.SetGroupKick import SetGroupKick
from modules.MessageUpload.GetBotInfo import GetBotInfo
from modules.MessageUpload.DeleteMsg import DeleteMsg

# 实例化
getBotInfo = GetBotInfo()

joiners = []


class Config:  # Class:程序设置
    # 程序版本号
    version = "1.0.0"
    # 服务器端口
    port = 8080
    # 服务器IP
    ip = "127.0.0.1"
    # 主人QQ
    master = 0
    # 管理员QQ
    admin = []
    # 机器人QQ
    bot = 0
    # 机器人昵称
    bot_name = ""
    # 调试模式
    debug = 0
    # 转发群聊消息给主人
    isForwardGroupMessageToMaster = 0

    # 读取配置文件
    def readFromFile(self, filePath):
        if not os.path.exists(filePath):
            return 0

        with open(filePath, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.version = data["version"]
            self.port = data["port"]
            self.ip = data["ip"]
            self.master = data["master"]
            self.admin = data["admin"]
            self.bot = data["bot"]
            self.bot_name = data["bot_name"]
            self.debug = data["debug"]

    # 保存配置文件
    def saveToFile(self, filePath):
        with open(filePath, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "version": self.version,
                    "port": self.port,
                    "ip": self.ip,
                    "master": self.master,
                    "admin": self.admin,
                    "bot": self.bot,
                    "bot_name": self.bot_name,
                    "debug": self.debug,
                },
                f,
                ensure_ascii=False,
                indent=4,
            )

    # 保存默认配置文件
    def saveDefaultConfig(self, filePath):
        with open(filePath, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "version": self.version,
                    "port": 8080,
                    "ip": "127.0.0.1",
                    "master": 0,
                    "admin": [],
                    "bot": 0,
                    "bot_name": "",
                    "debug": 0,
                },
                f,
                ensure_ascii=False,
                indent=4,
            )


class Variable:  # Class:程序变量
    # 是否第一次启动
    isFirstStart = True
    # 最新版本号
    latestVersion = ""
    # 配置文件路径，读取程序目录下的config文件夹下的config.json
    configFilePath = str(os.getcwd() + "\\data\\config.json")
    # Logo文件路径，读取程序目录下的config文件夹下的logo.txt
    logoFilePath = str(os.getcwd() + "\\data\\logo.txt")
    # 语录文件路径，读取程序目录下的config文件夹下的col.txt
    colFilePath = str(os.getcwd() + "\\data\\col.txt")
    # 白名单文件路径，读取程序目录下的config文件夹下的whitelist.txt
    whitelistFilePath = str(os.getcwd() + "\\data\\whitelist.txt")
    # 是否已经处理过最新收到的消息
    isLastMessageProcessed = False
    # 最新收到的消息
    lastMessage = ""
    # 最新收到的消息的发送者
    lastMessageSender = 0
    # 最新收到的消息的发送者的昵称
    lastMessageSenderNickname = ""
    # 是否为群消息
    isGroupMessage = False
    # 最新收到消息的群号
    lastMessageGroup = 0
    # 最新收到的消息的群昵称
    lastMessageGroupName = ""
    # 最新收到的消息的ID
    lastMessageID = 0


config = Config()  # 实例化Config类
variable = Variable()  # 实例化Variable类

# 逐行打印Logo
with open(variable.logoFilePath, "r", encoding="utf-8") as f:
    for line in f.readlines():
        print(line.strip("\n"))


def checkBeforeStart():  # 启动自检
    global sys

    # STEP 1: 检查Python版本
    if sys.version_info.major < 3:
        printc("Python版本过低，请使用Python 3.x", "E")
        return 0
    else:
        printc(
            "(STEP 1 / 3) Python版本检查通过 (Python "
            + str(sys.version_info.major)
            + "."
            + str(sys.version_info.minor)
            + ")",
            "I",
        )

    # STEP 2: 检查配置文件
    if config.readFromFile(variable.configFilePath) == 0:
        printc("配置文件读取失败", "E")
        printc("正在创建默认配置文件", "I")
        config.saveDefaultConfig(variable.configFilePath)
        printc("配置文件创建成功", "I")

    # 检查白名单文件是否存在
    if not os.path.exists(variable.whitelistFilePath):
        printc("白名单文件不存在，正在创建", "I")
        with open(variable.whitelistFilePath, "w", encoding="utf-8") as f:
            f.write("")
        printc("白名单文件创建成功", "I")
    else:
        printc("(STEP 2 / 3) 配置文件检查通过", "I")
        config.readFromFile(variable.configFilePath)
        printc("(STEP 2 / 3) 即将连接的服务器：" + config.ip + ":" + str(config.port), "I")
        printc("(STEP 2 / 3) 主人QQ：" + str(config.master), "I")
        printc("(STEP 2 / 3) 正在启动ZeroBot", "I")


async def main():
    try:
        async with websockets.connect(
            "ws://" + config.ip + ":" + str(config.port)
        ) as websocket:
            printc("(STEP 3 / 3) WebSocket服务器 连接成功", "I")
            printc("欢迎使用！", "I")
            print()  # 空行

            while True:
                # 等待服务器发送消息
                meessage = await websocket.recv()

                # 调试模式
                if config.debug == 1:
                    printc(meessage, "D")

                # 读取Json
                data = json.loads(meessage)

                # 若为首次启动，则获取机器人信息
                if variable.isFirstStart == True:
                    variable.isFirstStart = False
                    await websocket.send(getBotInfo.dump())

                # 若为机器人信息，则保存机器人信息
                if "data" in data:
                    if data["data"] != None:
                        if "nickname" in data["data"] and "user_id" in data["data"]:
                            config.bot_name = data["data"]["nickname"]
                            config.bot = data["data"]["user_id"]

                            printc("机器人信息获取成功", "I")
                            printc(" - 机器人QQ：" + str(data["data"]["user_id"]), "I")
                            printc(" - 机器人昵称：" + data["data"]["nickname"], "I")
                            print()

                            config.saveToFile(variable.configFilePath)

                # 展示收到的消息以及记录最新收到的消息
                if "post_type" in data:
                    if data["post_type"] != "meta_event":
                        if data["post_type"] == "message":  # 消息事件
                            if data["message_type"] == "group":  # 群聊消息
                                printc("收到群聊消息：", "I")
                                printc(" - 消息内容：" + data["message"], "I")
                                printc(
                                    " - 发送者："
                                    + (
                                        data["sender"]["card"]
                                        if data["sender"]["card"] != ""
                                        else data["sender"]["nickname"]
                                    ),
                                    "I",
                                )
                                printc(
                                    " - 发送者QQ：" + str(data["sender"]["user_id"]), "I"
                                )
                                printc(" - 群号：" + str(data["group_id"]), "I")
                                print()  # 空行

                                # 保存最新收到的消息
                                variable.isLastMessageProcessed = False
                                variable.lastMessage = data["message"]
                                variable.lastMessageSender = data["sender"]["user_id"]
                                variable.lastMessageSenderNickname = data["sender"][
                                    "card"
                                ]
                                variable.isGroupMessage = True
                                variable.lastMessageGroup = data["group_id"]
                                variable.lastMessageID = data["message_id"]

                                # 在下方添加指令
                                await websocket.send(
                                    Template(
                                        data["group_id"],
                                        data["message"],
                                    ).SendGroupMessage()
                                )

                    # 设置已经处理过最新收到的消息
                    variable.isLastMessageProcessed = True

    # 捕获错误
    except ConnectionRefusedError:
        printc("WebSocket服务器 连接失败", "E")
        printc("可能的原因：", "E")
        printc("1. 服务器未启动", "E")
        printc("2. 服务器IP或端口错误", "E")
    except Exception as e:
        # 输出错误信息
        printc("\n" + traceback.format_exc(), "E")
        printc("程序已退出", "E")
        os.system("pause")


checkBeforeStart()
asyncio.get_event_loop().run_until_complete(main())
