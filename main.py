import pygame
import mido
import tkinter as tk
from tkinter import filedialog
from threading import Thread
import sys

def select_file():
    """ 使用 Tkinter 彈出檔案選取視窗 """
    root = tk.Tk()
    root.withdraw()  # 隱藏主視窗
    file_path = filedialog.askopenfilename(
        title="請選取 MIDI 檔案",
        filetypes=[("MIDI files", "*.mid *.midi")]
    )
    root.destroy()
    return file_path

# 1. 取得檔案路徑
midi_path = select_file()
if not midi_path:
    print("未選取檔案，程式結束。")
    sys.exit()

# 2. 初始化 Pygame 繪圖與音訊
pygame.init()
screen = pygame.display.set_mode((800, 450))
pygame.display.set_caption(f"正在播放: {midi_path.split('/')[-1]}")

# 狀態與顏色設定
key_states = [0] * 128
WHITE, BLACK, BLUE = (255, 255, 255), (20, 20, 20), (0, 150, 255)

def midi_worker(path):
    """ 背景播放執行緒 """
    try:
        mid = mido.MidiFile(path)
        with mido.open_output() as outport:
            for msg in mid.play():
                outport.send(msg)
                if msg.type == 'note_on':
                    key_states[msg.note] = msg.velocity
                elif msg.type == 'note_off':
                    key_states[msg.note] = 0
    except Exception as e:
        print(f"播放出錯: {e}")

# 啟動背景播放
Thread(target=midi_worker, args=(midi_path,), daemon=True).start()

# 3. 主迴圈 (繪製介面)
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 繪製 88 鍵鋼琴
    margin = 20
    key_w = (800 - 2 * margin) // 52  # 52個白鍵
    # 這裡僅示範簡單的邏輯映射
    for i in range(21, 109):
        x = margin + (i - 21) * ((800 - 2 * margin) // 88)
        h = 100 + (key_states[i] * 0.5) # 根據力度改變高度感應
        color = BLUE if key_states[i] > 0 else WHITE
        pygame.draw.rect(screen, color, (x, 300 - (h-100), (800 // 88) - 1, h))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
