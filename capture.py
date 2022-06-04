# 画像書き込み
import cv2
# 型変換
import numpy as np
# スクリーンショット　（引数で座標指定可）
from PIL import ImageGrab
# WindowsAPI を触るため
import ctypes
# 時間計測
import time

# ウィンドウ名を探す用
import win32gui

# 初期設定
movie_time = 5         # 録画時間（秒）
window_name = 'Zoom ミーティング'   # ウィンドウの名前

# 開始時間の保存
sTime = time.time()
# 準備時間
while True:
    if time.time() - sTime > 3:
        break

# ウィンドウ名を探す用
# 現在アクティブなウィンドウ名を探す
process_list = []


def callback(handle, _):
    process_list.append(win32gui.GetWindowText(handle))


win32gui.EnumWindows(callback, None)
# ターゲットウィンドウ名を探す
for process_name in process_list:
    print(process_name)
    if window_name in process_name:
        hnd = win32gui.FindWindow(None, process_name)
        break
    else:
        # 見つからなかったら画面全体を取得
        # print('cant find')
        hnd = win32gui.GetDesktopWindow()
# ウィンドウサイズ取得
x0, y0, x1, y1 = win32gui.GetWindowRect(hnd)
x0 += 7
x1 -= 7
y1 -= 7
width = x1 - x0
height = y1 - y0

capSize = (width, height)

# コーデックの設定　今回は.mp4
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# 動画保存用
writer = cv2.VideoWriter('SC.mp4', fourcc, 10, capSize)
# gif用
images = []
# FPSのカウント用　1度だけ
count = 0
FirstFlag = True

# writerが開いている間、ループ
while (writer.isOpened()):
    # PIL Image から numpy配列 に変換してから書き込み
    img_bgr = np.asarray(ImageGrab.grab(bbox=(x0, y0, x1, y1)))
    img_rgb = img_bgr[:, :, [2, 1, 0]]    # BGR -> RGB順に
    writer.write(img_rgb)
    # gif用
    images.append(ImageGrab.grab(bbox=(x0, y0, x1, y1)))
    # FPS取得　１度だけ
    if FirstFlag:
        count += 1
        # 開始から１秒たったら、そのときのcountをFPSとする
        if time.time() - sTime > 1.0 + 3:
            writer.set(cv2.CAP_PROP_FPS, count)
            FirstFlag = False
    # 開始から録画時間（秒）で終了
    if time.time() - sTime > movie_time + 3:
        break

# gifファイルを保存
images[0].save('gif_date.gif', save_all=True,
               append_images=images[1:], optimize=False, duration=60, loop=0)

# writerの解放 -> 保存
writer.release()
