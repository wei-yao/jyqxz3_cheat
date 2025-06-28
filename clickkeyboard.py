from pynput import keyboard
import time

pressing = True
key_to_press = keyboard.KeyCode.from_char('3')  # 设置为数字3键

def on_press(key):
    global pressing
    if key == keyboard.Key.esc:  # 按ESC键停止
        pressing = False
        print("连点已停止")

if __name__ == "__main__":
    with keyboard.Listener(on_press=on_press) as listener:
        keyboard_controller = keyboard.Controller()
        while pressing:
            keyboard_controller.press(key_to_press)
            keyboard_controller.release(key_to_press)
            print("按键已按下")
            time.sleep(4)  # 间隔5秒，可调整
        print("线程已终止")
        listener.stop()
