# League of Legends Auto Move

## Functions I tried

```python
def MovePos():
    t = threading.currentThread()
    screen_size = pyautogui.size()

    Position = get_basic_pos(screen_size.width, screen_size.height)

    # for process in psutil.process_iter():
    #     print(process)

    while getattr(t, "do_run", True):
        for pos in Position:
            pyautogui.moveTo(pos[0], pos[1])
            time.sleep(3)


def main():
    countdown_t = threading.Thread(target=CountDown, args=(10,))
    movePos_t = threading.Thread(target=MovePos)
    countdown_t.start()
    movePos_t.start()

    countdown_t.join()
    movePos_t.do_run = False
```
