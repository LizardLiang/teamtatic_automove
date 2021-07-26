import psutil
import pyautogui
from pynput import mouse
import time
import threading
import json
import os
import math

game_name = "League of Legends.exe"
test_name = "LINE.exe"


class Auto_Move:
    def __init__(self, wait_time, loop_time, positions, actions):
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
        self.proc_wait = self.positions["porc-wait"]

    def Press_Mouse(self, right=False):
        button = "right" if right else "left"
        pyautogui.mouseDown(button=button)
        time.sleep(self.click_wait)
        pyautogui.mouseUp()

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
                    queue_t.do_run = False
                    self.is_playing = True

            if self.is_playing:
                # 跑等投降
                if not play_t.is_alive():
                    play_t = threading.Thread(target=self.Do_Play)
                    countdown_t = threading.Thread(target=self.CountDown)
                    self.timeup = False
                    countdown_t.start()
                    play_t.do_run = True
                    play_t.start()
                elif self.timeup:
                    # 如果正在玩 且 正在等待投降 且 時間到了
                    play_t.do_run = False
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
                    print("第 {} 場掛機".format(loop_cnt))
                    queue_t.do_run = True
                    queue_t.start()

    def Do_Queue(self):
        # 列隊中
        print("開始列隊")
        t = threading.currentThread()

        room_cnt = 0
        self.MoveTo(self.positions["room"])
        self.Press_Mouse()
        while getattr(t, "do_run", True):
            # 點擊 開始遊戲
            self.MoveTo(self.positions["new_game"])
            self.Press_Mouse()
            # 點擊 開始遊戲
            self.MoveTo(self.positions["start"])
            self.Press_Mouse()

            # 點擊 接受對戰
            self.MoveTo(self.positions["accept"])
            self.Press_Mouse()

            if room_cnt > 10:
                self.MoveTo(self.positions["room"])
                self.Press_Mouse()
                room_cnt = 0
            else:
                room_cnt = room_cnt + 1

    def Do_Play(self):
        # 遊玩中
        print("進入對戰")
        t = threading.currentThread()
        wander_cnt = 0
        while getattr(t, "do_run", True):
            if wander_cnt > (1800):
                wander_cnt = 0
                self.Wandering()
                if not getattr(t, "do_run", True):
                    break
            else:
                wander_cnt = wander_cnt + 1

            if self.actions == 1:
                self.D_Card()
            elif self.actions == 2:
                self.Shops()
                if not getattr(t, "do_run", True):
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


class Create_Setting:
    def __init__(self):
        self.file = None
        self.setting = {}
        self.record_cnt = 0

    def on_click(self, x, y, button, pressed):
        if mouse.Button.left == button:
            if not pressed:
                if self.record_cnt == 0:
                    self.setting["start"] = (x, y)
                    print("請點擊接受")
                elif self.record_cnt == 1:
                    self.setting["accept"] = (x, y)
                    jsonfile = json.dumps(self.setting)

                    print("校正完畢")

                    self.file.write(jsonfile)
                    self.file.close()
                    return False
                self.record_cnt = self.record_cnt + 1

    def Open_File(self):
        try:
            self.file = open("setting.json", "r")
            content = self.file.read()
            self.setting = json.loads(content)
            print(self.setting)
            self.file.close()
            print("讀取設定完畢")
            return True
        except:
            self.file = open("setting.json", "x")
            print("找不到初始化設定，請先進行設定")
            return False

    def Record_Pos(self):
        listener = mouse.Listener(on_click=self.on_click)
        print("請點擊開始對戰")
        listener.start()
        listener.join()

    def Reset_Setting(self):
        print("重新進行設定")
        if os.path.exists("setting.json"):
            os.remove("setting.json")

    def Get_Setting(self):
        return self.setting


if __name__ == "__main__":
    # main()
    create_setting = Create_Setting()
    res = create_setting.Open_File()

    if not res:
        create_setting.Record_Pos()

    while True:
        val = input("選擇工作\r\n1. 開始腳本\r\n2. 清除設定\r\n3. 檢視設定\r\n4. 離開\r\n")
        if val == "2":
            create_setting.Reset_Setting()
        elif val == "3":
            settings = create_setting.Get_Setting()
            print(
                "開始遊戲: {}\r\n接受遊戲: {}\r\n齒輪: {}".format(
                    settings["start"], settings["accept"], settings["gear"]
                )
            )
        elif val == "1":
            wait_time = input("輸入投降時間 單位: 分鐘\r\n")
            if wait_time == "":
                wait_time = 13

            loop_time = input("輸入掛機場數\r\n")
            if loop_time == "":
                loop_time = 10

            actions = input(
                "選擇對戰中動作\r\n \
                                1. D牌\r\n \
                                2. 購買/售出旗子\r\n \
                                3. 升級\r\n"
            )
            if actions == "":
                actions = 3

            print("本次掛機將在 {}分鐘後進行投降，並且遊玩 {}場".format(float(wait_time), int(loop_time)))
            auto_move = Auto_Move(
                float(wait_time),
                int(loop_time),
                create_setting.Get_Setting(),
                int(actions),
            )
            auto_move.Start_Loop()
        elif val == "4":
            break
