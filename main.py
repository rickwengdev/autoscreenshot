import os
import pyautogui
import time
import threading
from pynput import keyboard

# 保存圖片的資料夾
save_folder = 'photo'

# 確保保存資料夾存在
os.makedirs(save_folder, exist_ok=True)

# 判斷是否存在已保存的圖片
def check_existing_screenshots():
    existing_files = [f for f in os.listdir(save_folder) if f.endswith('.png')]
    if existing_files:
        print(f"Found existing screenshots: {existing_files}")
        response = input("Do you want to continue with the current numbering? (y/n): ").strip().lower()
        if response == 'y':
            # 根據現有檔案設定起始編號
            last_number = max(int(f.split('_')[1].split('.')[0]) for f in existing_files)
            return last_number + 1  # 繼續編號
        else:
            # 刪除所有舊圖片
            for f in existing_files:
                os.remove(os.path.join(save_folder, f))
            print("Deleted existing screenshots. Starting fresh.")
    return 1  # 如果沒有舊檔案，從1開始編號

# 用來追蹤截圖的編號
screenshot_counter = check_existing_screenshots()

# 自動點擊並截屏
def auto_click_and_screenshot():
    global screenshot_counter
    while True:
        screenshot = pyautogui.screenshot()  # 截圖
        pyautogui.click()  # 模擬鼠標點擊
        time.sleep(5)  # 等待12秒
        screenshot_name = os.path.join(save_folder, f'screenshot_{screenshot_counter}.png')  # 使用遞增編號命名文件
        screenshot.save(screenshot_name)  # 保存截圖
        print(f"Screenshot {screenshot_counter} saved to {screenshot_name}.")
        screenshot_counter += 1  # 增加編號

# 監聽鍵盤事件
def on_press(key):
    if key == keyboard.Key.esc:  # 如果按下 ESC 鍵
        print("Exiting...")
        return False  # 停止監聽
    try:
        if key.char == 'q':  # 如果按下 'q' 鍵
            print("Exiting...")
            return False  # 停止監聽
    except AttributeError:
        pass

# 提示退出信息
print("Press 'Q' or 'ESC' to exit the script.")

# 啟動自動點擊和截圖線程
click_thread = threading.Thread(target=auto_click_and_screenshot)
click_thread.start()

# 監聽鍵盤按鍵
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

# 等待點擊線程結束
click_thread.join()