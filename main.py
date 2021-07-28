import psutil
import pyautogui
from pynput import mouse
from pynput.mouse import Button

from python_imagesearch.imagesearch import imagesearch

import time
import threading
import json
import os
import math

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import ui

game_name = "League of Legends.exe"
test_name = "LINE.exe"

image_accept = "./images/accept.png"  # 接受對戰
image_again = "./images/again.png"  # 再來一場
image_bball = "./images/b_ball.png"  # 藍色晶球
image_closeesc = "./images/close_esc.png"  # 關閉設定
image_cost1 = "./images/cost_1.png"  # 一費牌
image_cost2 = "./images/cost_2.png"  # 二費牌
image_cost3 = "./images/cost_3.png"  # 三費牌
image_cost4 = "./images/cost_4.png"  # 四費牌
image_d = "./images/d.png"  # D牌
image_exp = "./images/exp.png"  # 升級
image_gear = "./images/gear.png"  # 齒輪
image_inroom = "./images/in_room.png"  # 進入組隊房間
image_modecon = "./images/mode_confirm.png"  # 模式確認
image_mode = "./images/mode.png"  # 選擇模式
image_queue = "./images/queue.png"  # 進行列隊
image_room = "./images/room.png"  # 回到房間
image_shopbl = "./images/shop_bl.png"  # 商店左下
image_shoptr = "./images/shop_tr.png"  # 商店右上
image_suraccept = "./images/sur_accept.png"  # 投降確認
image_sur = "./images/sur.png"  # 投降按紐
image_wball = "./images/w_ball.png"  # 白色晶球


class Auto_Move(threading.Thread):
    def __init__(
        self, wait_time, loop_time, positions, wander, d, exp, shop, name="Auto_Move"
    ):
        self._stopevent = threading.Event()
        self.wait_time = float(wait_time)
        self.loop_time = int(loop_time)
        self.positions = positions
        self.is_playing = False
        self.timeup = False
        self.wander = wander
        self.d = d
        self.exp = exp
        self.shop = shop
        self.click_wait = self.positions["click-wait"]
        self.drag_wait = self.positions["drag-wait"]
        self.move_wait = self.positions["move-wait"]
        self.walk_wait = self.positions["walk-wait"]
        self.proc_wait = self.positions["proc-wait"]
        self.kill_flag = False
        self.cnt = 0

        self.room_cnt = 0  # 幾次列隊之後要按回到組隊房間
        self.wander_cnt = 0  # 對戰中幾次動作之後要遊走
        threading.Thread.__init__(self, name=name)

    def Press_Mouse(self, right=False):
        button = "right" if right else "left"
        pyautogui.mouseDown(button=button)
        time.sleep(self.click_wait)
        pyautogui.mouseUp(button=button)
        time.sleep(self.click_wait)

    def CountDown(self):
        print("開始投降")
        self.timeup = True

    def run(self):
        loop_cnt = 0

        # 三個狀態 三個線程
        self.countdown_t = threading.Timer(self.wait_time * 60, self.CountDown)

        self.room_cnt = 0

        print("第 {} 場掛機".format(loop_cnt + 1))
        # 依照使用者輸入 進行場次的對戰
        while loop_cnt < self.loop_time and not self._stopevent.isSet():
            find_game = False
            for proc in psutil.process_iter():
                if proc.name() == game_name:
                    find_game = True
                    if not self.is_playing:
                        # 找到這個執行緒 代表遊戲開始
                        print("進入對戰")
                        self.countdown_t.start()
                        self.is_playing = True

            # 如果沒有找到執行緒，且目前為遊玩中，表示遊戲結束
            if not find_game and self.is_playing:
                loop_cnt = loop_cnt + 1

                # 如果正在玩 且 正在等待投降 且 時間到了
                self.room_cnt = 0
                self.wander_cnt = 0
                self.countdown_t.join()
                self.is_playing = False
                self.timeup = False
                print("對戰結束初始化完成")

            if self.is_playing:
                # 跑等投降
                if not self.timeup:
                    self.Do_Play()
                    time.sleep(1)
                # 如果遊玩中，但時間到了，進行投降
                elif self.timeup:
                    self.Surrender_Task()

            else:
                # 跑列隊
                print("do queue task")
                self.Do_Queue()

        self.is_playing = True
        self.timeup = True

    def Find_(self, pic):
        return pyautogui.locateCenterOnScreen(pic, confidence=0.8)

    def Do_Queue(self):
        # 列隊中
        start_pos = self.Find_(image_queue)

        if not start_pos:
            room_pos = self.Find_(image_room)

            if room_pos != None:
                print("找到建立遊戲")
                # 點擊 開始遊戲
                self.MoveTo(room_pos)
                self.Press_Mouse()

            mode_pos = self.Find_(image_mode)

            if mode_pos != None:
                print("找到模式")
                self.MoveTo(mode_pos)
                self.Press_Mouse()

            confirm_pos = self.Find_(image_modecon)

            if confirm_pos != None:
                print("找到建立模式")
                self.MoveTo(confirm_pos)
                self.Press_Mouse()

        start_pos = self.Find_(image_queue)

        if start_pos != None:
            print("找到開始列隊")
            # 點擊 開始遊戲
            self.MoveTo([start_pos[0] + 10, start_pos[1]])
            self.Press_Mouse()

        accept_pos = self.Find_(image_accept)

        if accept_pos != None:
            print("找到接受對戰")
            # 點擊 接受對戰
            self.MoveTo(self.positions["accept"])
            self.Press_Mouse()

    def Do_Play(self):
        # 遊玩中
        if self.d:
            self.D_Card()
        if self.shop:
            self.Shops()
            if self.timeup:
                return
            self.Sell_Card()
        if self.exp:
            self.Get_Exp()

    def Surrender_Task(self):
        gear_pos = self.Find_(image_gear)

        if gear_pos != None:
            print("找到齒輪")
            # 移到齒輪
            self.MoveTo(self.positions["gear"])
            # 按左鍵
            self.Press_Mouse()

        sur_pos = self.Find_(image_sur)

        if sur_pos != None:
            # 移到投降
            self.MoveTo(self.positions["surrender"])
            # 按左鍵
            self.Press_Mouse()

        sur_pos = self.Find_(image_suraccept)

        if sur_pos != None:
            print("找到投降確認")
            # 移到確定投降
            self.MoveTo(self.positions["sur_accept"])
            # 按左鍵
            self.Press_Mouse()

        close_pos = self.Find_(image_closeesc)

        if close_pos != None:
            # 移至關閉設定
            self.MoveTo(self.positions["close_setting"])
            # 按下左鍵
            self.Press_Mouse()

    def D_Card(self):
        pos = self.Find_(image_d)
        if pos != None:
            print("找到 d 牌")
            self.MoveTo(pos)
            self.Press_Mouse()

    def Get_Exp(self):
        pos = self.Find_(image_exp)
        if pos != None:
            print("找到升級")
            self.MoveTo(pos)
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

    def get_remain_time(self):
        return self.wait_time - self.cnt

    def kill_(self, timeout=None):
        self.countdown_t.cancel()
        self._stopevent.set()
        threading.Thread.join(self, timeout)
        return True


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


class Main(QMainWindow, ui.Ui_JustAScript):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.settings = Create_Setting()
        self.settings.Open_File()

        self.setting = self.settings.Get_Setting()

        self.use_wander = False
        self.use_d = False
        self.use_exp = False
        self.use_shop = False

        self.wandering.stateChanged.connect(self.set_wander)
        self.d_card.stateChanged.connect(self.set_d)
        self.exp.stateChanged.connect(self.set_exp)
        self.shop.stateChanged.connect(self.set_shop)

        self.surrs = self.setting["default"]["surrender-time"]
        self.loops = self.setting["default"]["loop-times"]

        self.sur_time.setValue(self.surrs)
        self.loop_time.setValue(self.loops)

        self.sur_time.valueChanged.connect(self.set_sur_value)
        self.loop_time.valueChanged.connect(self.set_loop_value)

        self.start.clicked.connect(self.Start)
        self.stop.clicked.connect(self.Stop)

        self.loop = Auto_Move(
            self.surrs,
            self.loops,
            self.setting,
            self.use_wander,
            self.use_d,
            self.use_exp,
            self.use_shop,
        )

    def set_sur_value(self):
        self.surrs = int(self.sur_time.value())

    def set_loop_value(self):
        self.loops = int(self.loop_time.value())

    def set_wander(self):
        if self.wandering.isChecked():
            self.use_wander = True
        else:
            self.use_wander = False

    def set_d(self):
        self.use_d = True if self.d_card.isChecked() else False

    def set_exp(self):
        self.use_exp = True if self.exp.isChecked() else False

    def set_shop(self):
        self.use_shop = True if self.shop.isChecked() else False

    def Start(self):
        self.loop = Auto_Move(
            self.surrs,
            self.loops,
            self.setting,
            self.use_wander,
            self.use_d,
            self.use_exp,
            self.use_shop,
        )
        self.loop.start()

    def closeEvent(self, event):
        self.loop.kill_()
        print("close")

    def Stop(self):
        self.loop.kill_()


if __name__ == "__main__":
    print("正式版本 v1.0")
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
