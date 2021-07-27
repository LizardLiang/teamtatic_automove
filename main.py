import psutil
import pyautogui
from pynput import mouse
from pynput.mouse import Button
import time
import threading
import json
import os
import math

game_name = "League of Legends.exe"
test_name = "LINE.exe"


class Auto_Move:
    def __init__(self, wait_time, loop_time, positions, actions, calc):
        self.wait_time = float(wait_time)
        self.loop_time = int(loop_time)
        self.positions = positions
        self.is_playing = False
        self.timeup = False
        self.actions = actions
        self.click_wait = self.positions["click-wait"]
        self.drag_wait = self.positions["drag-wait"]
        self.move_wait = self.positions["move-wait"]
        self.walk_wait = self.positions["walk-wait"]
        self.proc_wait = self.positions["proc-wait"]
        self.calc = calc

    def Press_Mouse(self, right=False):
        button = "right" if right else "left"
        pyautogui.mouseDown(button=button)
        time.sleep(self.click_wait)
        pyautogui.mouseUp(button=button)

    def CountDown(self):
        print("將於 {}分鐘後進行投降".format(self.wait_time))
        time.sleep(math.floor(self.wait_time * 60))
        self.timeup = True
        print("開始投降")

    def Start_Loop(self):
        loop_cnt = 0

        # 三個狀態 三個線程
        queue_t = threading.Thread(target=self.Do_Queue)
        play_t = threading.Thread(target=self.Do_Play)
        countdown_t = threading.Thread(target=self.CountDown)

        # 依照使用者輸入 進行場次的對戰
        while loop_cnt < self.loop_time:
            for proc in psutil.process_iter():
                if proc.name() == game_name and not self.is_playing:
                    # 找到這個執行緒 代表遊戲開始
                    self.is_playing = True

            if self.is_playing:
                # 跑等投降
                if not play_t.is_alive():
                    play_t = threading.Thread(target=self.Do_Play)
                    countdown_t = threading.Thread(target=self.CountDown)
                    self.timeup = False
                    countdown_t.start()
                    play_t.start()
                    while not play_t.is_alive():
                        pass
                elif self.timeup:
                    # 如果正在玩 且 正在等待投降 且 時間到了
                    tmp = True
                    while tmp or play_t.is_alive():
                        tmp = False
                        for proc in psutil.process_iter():
                            if proc.name() == game_name:
                                tmp = True
                        time.sleep(self.proc_wait)

                    loop_cnt = loop_cnt + 1

            else:
                # 跑列隊
                if not queue_t.is_alive():
                    queue_t = threading.Thread(target=self.Do_Queue)
                    print("第 {} 場掛機".format(loop_cnt + 1))
                    queue_t.start()
                    while not queue_t.is_alive():
                        pass

    def Do_Queue(self):
        # 列隊中
        print("開始列隊")
        t = threading.currentThread()

        room_cnt = 0
        while not self.is_playing:
            # 點擊 開始遊戲
            self.MoveTo(self.calc.calc_client(self.positions["new_game"]))
            self.Press_Mouse()
            # 點擊 開始遊戲
            self.MoveTo(self.calc.calc_client(self.positions["start"]))
            self.Press_Mouse()

            # 點擊 接受對戰
            self.MoveTo(self.calc.calc_client(self.positions["accept"]))
            self.Press_Mouse()

            if room_cnt > 10:
                self.MoveTo(self.calc.calc_client(self.positions["room"]))
                self.Press_Mouse()
                room_cnt = 0
            else:
                room_cnt = room_cnt + 1

    def Do_Play(self):
        # 遊玩中
        print("進入對戰")
        t = threading.currentThread()
        wander_cnt = 0
        while not self.timeup:
            if wander_cnt > self.positions["walk-cooldown"] and self.actions != 0:
                wander_cnt = 0
                self.Wandering()
                if self.timeup:
                    break
            else:
                wander_cnt = wander_cnt + 1

            if self.actions == 1:
                self.D_Card()
            elif self.actions == 2:
                self.Shops()
                if not self.timeup:
                    break
                self.Sell_Card()
            elif self.actions == 3:
                self.Get_Exp()

        tmp = True
        while tmp:
            tmp = False
            self.Surrender_Task()
            for proc in psutil.process_iter():
                if proc.name() == game_name:
                    tmp = True
        # 遊戲結束 轉為列隊
        self.is_playing = False

    def Surrender_Task(self):
        # 移到齒輪
        self.MoveTo(self.positions["gear"])
        # 按左鍵
        self.Press_Mouse()
        # 移到投降
        self.MoveTo(self.positions["surrender"])
        # 按左鍵
        self.Press_Mouse()
        # 移到確定投降
        self.MoveTo(self.positions["sur_accept"])
        # 按左鍵
        self.Press_Mouse()
        # 移至關閉設定
        self.MoveTo(self.positions["close_setting"])
        # 按下左鍵
        self.Press_Mouse()

        time.sleep(10)

    def D_Card(self):
        self.MoveTo(self.positions["d_card"])
        self.Press_Mouse()

    def Get_Exp(self):
        self.MoveTo(self.positions["exp"])
        self.Press_Mouse()

    def Shops(self):
        for index, card in enumerate(self.positions["shops"]):
            print("購買 第{}個旗子".format(index + 1))
            self.MoveTo(card)
            self.Press_Mouse()

    def Sell_Card(self):
        for index, card in enumerate(self.positions["owned"]):
            print("售出 第{}個旗子".format(index + 1))
            self.MoveTo(card)
            self.DragTo(self.positions["sell_pos"])

    def Wandering(self):
        for index, pos in enumerate(self.positions["wandering"]):
            print(pos)
            self.WalkThere(pos)
            time.sleep(self.walk_wait)

    def MoveTo(self, position):
        pyautogui.moveTo(position[0], position[1])
        time.sleep(self.move_wait)

    def WalkThere(self, pos):
        self.MoveTo(pos)
        self.Press_Mouse(True)

    def DragTo(self, position):
        pyautogui.mouseDown()
        time.sleep(self.drag_wait)
        pyautogui.moveTo(position)
        time.sleep(self.drag_wait)
        pyautogui.mouseUp()
        time.sleep(self.drag_wait)


class Auto_Cal:
    def __init__(self, client, game):
        # client
        # 1800 x 900, 1280 x 720, 1024 x 576
        if client == 1:
            self.c_width = 1800
            self.c_height = 900
        elif client == 2:
            self.c_width = 1280
            self.c_height = 720
        elif client == 3:
            self.c_width = 1024
            self.c_height = 576

        # game
        # 1920 x 1080, 2560 x 1440, 3840 x 2160
        if game == 1:
            self.g_width = 1920
            self.g_height = 1080
        elif game == 2:
            self.g_width = 2560
            self.g_height = 1440
        elif game == 3:
            self.g_width = 3840
            self.g_height = 2160

        self.w_zero = 1920 / 2
        self.h_zero = 1080 / 2

    # 計算客戶端按鈕位置
    def calc_client(self, pos):
        new_w_zero = self.g_width / 2
        new_h_zero = self.g_height / 2

        # 原本的距離 x 客戶端的比率 加到新的中心點
        new_w = (pos[0] - self.w_zero) * (self.c_width / 1280) + new_w_zero
        new_h = (pos[1] - self.h_zero) * (self.c_height / 720) + new_h_zero

        return [new_w, new_h]


class Create_Setting:
    def __init__(self):
        self.file = None
        self.setting = {}

    def Open_File(self):
        try:
            self.file = open("setting.json", "r")
            content = self.file.read()
            self.setting = json.loads(content)
            self.file.close()
            print("讀取設定完畢")
            return True
        except:
            print("找不到初始化設定，請重新下載 setting.json")
            return False

    def Get_Setting(self):
        return self.setting

    def Write_Setting(self, settings):
        content = json.dumps(settings)

        f = open("setting.json", "w")
        f.write(content)
        f.close()
        print("已存入新預設值")


class Calibrate:
    def __init__(self, setting):
        self.setting = setting
        self.cnt = 0

    def start(self):
        with mouse.Listener(on_click=self.listener) as listener:
            print("開始校正\r\n請在開始列隊點擊右鍵\r\n")
            listener.join()

    def listener(self, x, y, button, pressed):
        if pressed and button == Button.right:
            if self.cnt == 0:
                self.setting["start"] = [x, y]
                print("請在接受對戰點擊右鍵")
            elif self.cnt == 1:
                self.setting["accept"] = [x, y]
                print("請等待遊戲開始後")
                print("請以右鍵點擊 D牌按紐")
            elif self.cnt == 2:
                self.setting["d_card"] = [x, y]
                print("請以右鍵點擊升級")
            elif self.cnt == 3:
                self.setting["exp"] = [x, y]
                print("請從左至右以右鍵點擊商店卡牌")
            elif self.cnt == 4:
                self.setting["shops"][0] = [x, y]
                print("下一個位置")
            elif self.cnt == 5:
                self.setting["shops"][1] = [x, y]
                print("下一個位置")
            elif self.cnt == 6:
                self.setting["shops"][2] = [x, y]
                print("下一個位置")
            elif self.cnt == 7:
                self.setting["shops"][3] = [x, y]
                print("下一個位置")
            elif self.cnt == 8:
                self.setting["shops"][4] = [x, y]
                print("請依序以右鍵點擊手牌位置")
            elif self.cnt == 9:
                self.setting["owned"][0] = [x, y]
                print("下一個位置")
            elif self.cnt == 10:
                self.setting["owned"][1] = [x, y]
                print("下一個位置")
            elif self.cnt == 11:
                self.setting["owned"][2] = [x, y]
                print("下一個位置")
            elif self.cnt == 12:
                self.setting["owned"][3] = [x, y]
                print("下一個位置")
            elif self.cnt == 13:
                self.setting["owned"][4] = [x, y]
                print("下一個位置")
            elif self.cnt == 14:
                self.setting["owned"][5] = [x, y]
                print("下一個位置")
            elif self.cnt == 15:
                self.setting["owned"][6] = [x, y]
                print("下一個位置")
            elif self.cnt == 16:
                self.setting["owned"][7] = [x, y]
                print("下一個位置")
            elif self.cnt == 17:
                self.setting["owned"][8] = [x, y]
                print("請用右鍵點擊售出卡牌的位置")
            elif self.cnt == 18:
                self.setting["sell_pos"] = [x, y]
                print("請用右鍵點擊齒輪位置")
            elif self.cnt == 19:
                self.setting["gear"] = [x, y]
                print("請用右鍵點擊投降位置")
            elif self.cnt == 20:
                self.setting["surrender"] = [x, y]
                print("請用右鍵點擊接受投降位置")
            elif self.cnt == 21:
                self.setting["sur_accept"] = [x, y]
                print("請用右鍵點擊再來一場")
            elif self.cnt == 22:
                self.setting["new_game"] = [x, y]
                print("請用右鍵點擊回到組隊房間")
            elif self.cnt == 23:
                self.setting["room"] = [x, y]
                f = open("setting.json", "w")
                content = json.dumps(self.setting)
                f.write(content)
                f.close()
                print("校正完畢")
                return False
            self.cnt = self.cnt + 1


c_reso_msg = ["1800 x 900", "1280 x 760", "1024 x 576"]
g_reso_msg = ["1920 x 1080", "2560 x 1440", "3840 x 2160"]
action_msg = ["不動作", "D牌", "購買/售出 棋子", "升級"]

if __name__ == "__main__":
    print("正式版本 v1.0")
    create_setting = Create_Setting()
    res = create_setting.Open_File()

    if not res:
        create_setting.Record_Pos()

    while True:
        val = input("選擇工作\r\n1. 開始腳本\r\n2. 重新校正\r\n3. 離開\r\n")
        if val == "1":
            setting = create_setting.Get_Setting()
            use_default = input("使用預設值(是)?\r\n1. 是\r\n2. 否\r\n")
            wait_time, loop_time, actions, c_reso, g_reso = "", "", "", "", ""

            if use_default == "2":
                wait_time = input("輸入投降時間 單位: 分鐘\r\n")
                if wait_time == "":
                    wait_time = 13

                loop_time = input("輸入掛機場數\r\n")
                if loop_time == "":
                    loop_time = 10

                actions = input(
                    """選擇對戰中動作\r\n0.不動作\r\n1. D牌\r\n2. 購買/售出旗子\r\n3. 升級\r\n"""
                )
                if actions == "":
                    actions = 3

                c_reso = input(
                    "請選擇客戶端大小\r\n1. 1800 x 900\r\n2. 1280 x 720\r\n3. 1024 x 576\r\n"
                )
                if c_reso == "" or int(c_reso) > 3 or int(c_reso) < 1:
                    c_reso = 2

                g_reso = input(
                    "請選擇螢幕大小\r\n1. 1920 x 1080\r\n2. 2560 x 1440\r\n3. 3840 x 2160\r\n"
                )
                if g_reso == "" or int(g_reso) > 3 or int(g_reso) < 1:
                    g_reso = 1

                values = setting["default"]
                values["surrender-time"] = float(wait_time)
                values["loop-times"] = int(loop_time)
                values["action"] = int(actions)
                values["client-reso"] = int(c_reso)
                values["monitor-reso"] = int(g_reso)

                setting["default"] = values
                create_setting.Write_Setting(setting)

            else:
                values = setting["default"]
                wait_time = values["surrender-time"]
                loop_time = values["loop-times"]
                actions = values["action"]
                c_reso = values["client-reso"]
                g_reso = values["monitor-reso"]

            print("本次掛機將在 {}分鐘後進行投降，並且遊玩 {}場".format(float(wait_time), int(loop_time)))
            print(
                "設定:\r\n動作: {}\r\n客戶端解析度: {}\r\n螢幕解析度: {}\r\n".format(
                    action_msg[int(actions)],
                    c_reso_msg[int(c_reso) - 1],
                    g_reso_msg[int(g_reso) - 1],
                )
            )

            auto_move = Auto_Move(
                float(wait_time),
                int(loop_time),
                setting,
                int(actions),
                Auto_Cal(int(c_reso), int(g_reso)),
            )
            auto_move.Start_Loop()
        elif val == "2":
            calibrate = Calibrate(create_setting.Get_Setting())
            calibrate.start()
        elif val == "3":
            break
