import psutil
import pyautogui
from pynput import mouse
import time
import threading
import json
import os
import math


class Auto_Move:
    def __init__(self, wait_time, loop_time, positions):
        self.wait_time = wait_time
        self.loop_time = loop_time
        self.positions = positions
        self.is_playing = False
        self.timeup = False

    def CountDown(self):
        print("將於 分鐘後進行投降".format(self.wait_time))
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
                if proc.name() == "League of Legends.exe" and not self.is_playing:
                    # 找到這個執行緒 代表遊戲開始
                    queue_t.do_run = False
                    self.is_playing = True

            if self.is_playing:
                # 跑等投降
                if not play_t.is_alive():
                    countdown_t.start()
                    play_t.do_run = True
                    play_t.start()
                    loop_cnt = loop_cnt + 1
                elif self.timeup:
                    # 如果正在玩 且 正在等待投降 且 時間到了
                    play_t.do_run = False

            else:
                # 跑列隊
                if not queue_t.is_alive():
                    print("第 {} 場掛機".format(loop_cnt))
                    queue_t.do_run = True
                    queue_t.start()

    def Do_Queue(self):
        # 列隊中
        print("開始列隊")
        t = threading.currentThread()

        while getattr(t, "do_run", True):
            # 點擊 開始遊戲
            pyautogui.moveTo(
                self.positions["new_game"][0], self.positions["new_game"][1]
            )
            pyautogui.click()
            time.sleep(5)
            # 點擊 開始遊戲
            pyautogui.moveTo(self.positions["start"][0], self.positions["start"][1])
            pyautogui.click()
            time.sleep(5)

            # 點擊 接受對戰
            pyautogui.moveTo(self.positions["accept"][0], self.positions["accept"][1])
            pyautogui.click()
            time.sleep(5)

    def Do_Play(self):
        # 遊玩中
        print("進入對戰")
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            pyautogui.move(250, 0)
            time.sleep(5)
            pyautogui.click(button="right")
            time.sleep(5)
            pyautogui.move(-250, 0)
            time.sleep(5)
            pyautogui.click(button="right")
            time.sleep(5)

        print("對戰結束，進行下一場對戰")
        pyautogui.press("esc")
        time.sleep(3)
        pyautogui.moveTo(self.positions["surrender"][0], self.positions["surrender"][1])
        time.sleep(3)
        pyautogui.click()
        time.sleep(3)
        pyautogui.moveTo(
            self.positions["sur_accept"][0], self.positions["sur_accept"][1]
        )
        time.sleep(3)
        pyautogui.click()

        # 遊戲結束 轉為列隊
        self.is_playing = False


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
                "開始遊戲: {}\r\n接受遊戲: {}\r\n".format(settings["start"], settings["accept"])
            )
        elif val == "1":
            wait_time = input("輸入投降時間 單位: 分鐘\r\n")
            if wait_time == "":
                wait_time = 13

            loop_time = input("輸入掛機場數\r\n")
            if loop_time == "":
                loop_time = 10

            print("本次掛機將在 {}分鐘後進行投降，並且遊玩 {}場".format(float(wait_time), int(loop_time)))
            auto_move = Auto_Move(
                float(wait_time), int(loop_time), create_setting.Get_Setting()
            )
            auto_move.Start_Loop()
        elif val == "4":
            break
