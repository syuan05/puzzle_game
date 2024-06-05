import cv2 as cv
import numpy as np
import random
import math

# 讀取圖片
src = cv.imread("1.png")
# 獲取圖片的高度、寬度和通道數
h, w, c = src.shape

# 定義行數和列數
row = 3
col = 3

# 計算每個方塊的高度和寬度
offset_h = h // row
offset_w = w // col

# 初始化點擊狀態和點擊索引
firstClick = False
clickIdx = [0, 0]

# 初始化方塊列表
tileList = []

# 計算點擊位置對應的方塊索引
def calPicIdx(x, y):
    i = y // offset_h  # 計算所在行
    j = x // offset_w  # 計算所在列
    idx = int(i * col + j)  # 計算方塊索引
    print(f"i: {i}, j: {j}, idx: {idx}")
    return idx

# 處理滑鼠事件
def onMouse(event, x, y, flags, params):
    global firstClick
    if event == cv.EVENT_LBUTTONDOWN:  # 如果是左鍵點擊
        print(f"left button down: {x}, {y}")
        idx = calPicIdx(x, y)  # 計算點擊位置對應的方塊索引
        firstClick = not firstClick  # 切換點擊狀態
        if firstClick:
            clickIdx[0] = idx  # 記錄第一次點擊的方塊索引
        else:
            clickIdx[1] = idx  # 記錄第二次點擊的方塊索引
            # 交換兩個方塊的位置
            tileList[clickIdx[0]], tileList[clickIdx[1]] = tileList[clickIdx[1]], tileList[clickIdx[0]]
            # 創建一個空白圖像來存放交換後的結果
            dst = np.zeros((h, w, c), np.uint8)
            for i in range(row):
                for j in range(col):
                    # 根據方塊索引重新組合圖片
                    dst[i*offset_h:(i+1)*offset_h, j*offset_w:(j+1)*offset_w] = tileList[i*col+j]
            cv.imshow("dst", dst)  # 顯示重組後的圖像

            # 比較當前圖像與原圖像的差異
            difference = cv.subtract(dst, src2)
            result = not np.any(difference)  # 如果差異全為零，說明兩張圖片一致
            # print(f"result: {result}")
            print(difference)

# --------------將圖片切成 n*n 方塊--------------
for i in range(row):
    for j in range(col):
        # 提取每個方塊並添加到方塊列表中
        tile = src[i*offset_h:(i+1)*offset_h, j*offset_w:(j+1)*offset_w]
        tileList.append(tile)

# --------------隨機打亂方塊--------------------
random.shuffle(tileList)

# debug顯示每個方塊
# for k, tile in enumerate(tileList):
#     cv.imshow(f"tile{k}", tile)

# 創建一個空白圖像來存放打亂後的方塊
dst = np.zeros((h, w, c), np.uint8)
for i in range(row):
    for j in range(col):
        # 將打亂後的方塊重新組合成圖像
        dst[i*offset_h:(i+1)*offset_h, j*offset_w:(j+1)*offset_w] = tileList[i*col+j]
# 創建窗口並設置滑鼠回調函數
cv.namedWindow("dst")
cv.setMouseCallback("dst", onMouse)
cv.imshow("dst", dst)

# -------------匹配原圖與打亂的圖--------------
# 複製原圖
src2 = src.copy()
# # 在每行之間添加黑色邊界
# for i in range(1, row):
#     src2[i*offset_h-1:i*offset_h] = np.zeros((1, w, 3), np.uint8)
# # 在每列之間添加黑色邊界
# for j in range(1, col):
#     src2[:, j*offset_w-1:j*offset_w] = np.zeros((h, 1, 3), np.uint8)
# # cv.imshow("src2", src2)

# 等待按鍵事件
cv.waitKey(0)
