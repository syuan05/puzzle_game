import numpy as np
import cv2
import random
import time

canva = cv2.imread("background.jpg")
picture = 1
degree = 3
squareList = []
firstClick = False
clickIdx = [0, 0]
block_height = 0
block_width = 0
height = 0
width = 0
c = 0
step = 0
end_game = False
copy_image = cv2.imread("1.png")
start_time = time.monotonic()
spend_time = 0.00
current_time = 0.00
remain_time = 0.00
count_time = 20.00


def reset_base():
    global start_time
    global remain_time
    global spend_time
    global current_time
    global count_time
    global squareList
    global firstClick
    global step
    start_time = time.monotonic()
    spend_time = 0.00
    current_time = 0.00
    remain_time = 0.00
    count_time = 20.00
    squareList = []
    firstClick = False
    step = 0
    

# 難易度&照片選擇
def button_select(event, x, y, flags, param):
    global degree
    global picture
    global canva
    if event == cv2.EVENT_LBUTTONDOWN:
        if 116 <= x <= 285 and 36 <= y <= 205:
            picture = 1
        if 316 <= x <= 485 and 36 <= y <= 205:
            picture = 2
        if 516 <= x <= 685 and 36 <= y <= 205:
            picture = 3
        if 116 <= x <= 285 and 235 <= y <= 403:
            picture = 4
        if 316 <= x <= 485 and 235 <= y <= 403:
            picture = 5
        if 516 <= x <= 685 and 235 <= y <= 403:
            picture = 6
        if 170 <= x <= 230 and 430 <= y <= 460:
            degree = 3
        if 370 <= x <= 430 and 430 <= y <= 460:
            degree = 4
        if 570 <= x <= 630 and 430 <= y <= 460:
            degree = 5
        if 690 <= x <= 790 and 445 <= y <= 485:
            canva = cv2.imread("background.jpg")
            cv2.putText(canva, "PUZZLE GAME!", (157, 150), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 0), 2)
            cv2.rectangle(canva, (320, 190), (480, 240), (0, 240, 204), -1)
            cv2.putText(canva, "Select", (355, 225), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.rectangle(canva, (320, 270), (480, 320), (0, 230, 140), -1)
            cv2.putText(canva, "Start", (360, 305), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            reset_base()
            cv2.setMouseCallback('Game!', button_click)
        print(f"圖片:{picture} 難易度:{degree}")


# 難易度&照片選擇介面
def button_click(event, x, y, flags, param):
    global picture
    global canva
    if event == cv2.EVENT_LBUTTONDOWN:
        if 320 <= x <= 480 and 190 <= y <= 240:
            canva = cv2.imread("select.png")
            cv2.rectangle(canva, (170, 430), (230, 460), (210, 210, 226), -1)
            cv2.putText(canva, "3x3", (185, 450), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 1)
            cv2.rectangle(canva, (370, 430), (430, 460), (210, 210, 226), -1)
            cv2.putText(canva, "4x4", (385, 450), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 1)
            cv2.rectangle(canva, (570, 430), (630, 460), (210, 210, 226), -1)
            cv2.putText(canva, "5x5", (585, 450), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 1)
            cv2.rectangle(canva, (690, 445), (790, 485), (159, 181, 162), -1)
            cv2.putText(canva, "BACK", (705, 470), cv2.FONT_HERSHEY_TRIPLEX, 0.8, (255, 255, 255), 1)
            cv2.setMouseCallback('Game!', button_select)
        elif 320 <= x <= 480 and 270 <= y <= 320:
            if picture == 1:
                image = cv2.imread("1.png")
            elif picture == 2:
                image = cv2.imread("2.png")
            elif picture == 3:
                image = cv2.imread("3.png")
            elif picture == 4:
                image = cv2.imread("4.png")
            elif picture == 5:
                image = cv2.imread("5.png")
            elif picture == 6:
                image = cv2.imread("6.png")
            split_picture(image)
            cv2.setMouseCallback('Game!', move_square) 


# 更新遊戲
def reset_game(event, x, y, flags, param):
    global canva
    global squareList
    global end_game
    if event == cv2.EVENT_LBUTTONDOWN:
        if 200 <= x <= 350 and 480 <= y <= 520:
            canva = cv2.imread("background.jpg")
            cv2.putText(canva, "PUZZLE GAME!", (157, 150), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 0), 2)
            cv2.rectangle(canva, (320, 190), (480, 240), (0, 240, 204), -1)
            cv2.putText(canva, "Select", (355, 225), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.rectangle(canva, (320, 270), (480, 320), (0, 230, 140), -1)
            cv2.putText(canva, "Start", (360, 305), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            reset_base()
            cv2.setMouseCallback('Game!', button_click)
        elif 400 <= x <= 500 and 480 <= y <= 520:
            end_game = True


# 計算所在格數
def calIdx(x, y):
    i = y // block_height
    j = x // block_width
    idx = int(i * degree + j)
    return idx


# 移動方塊
def move_square(event, x, y, flags, param):
    global firstClick
    global canva
    global squareList
    global clickIdx
    global firstClick
    global step
    global count_time
    global start_time
    global remain_time
    global spend_time
    current_time = 20.00
    if event == cv2.EVENT_LBUTTONDOWN:
        current_time = 20.00
        firstClick = not firstClick
        idx = calIdx(x, y)
        print(idx)
        if firstClick:                   # 第一次被點擊的方塊編號
            clickIdx[0] = idx
        else:
            step += 1
            clickIdx[1] = idx
            # 交換
            squareList[clickIdx[0]], squareList[clickIdx[1]] = squareList[clickIdx[1]], squareList[clickIdx[0]]
            # print(f"height = {height}, width = {width}")
            canva = np.zeros((height, width, c), np.uint8)
            for i in range(degree):
                for j in range(degree):
                    canva[i * block_height:(i + 1) * block_height, j * block_width:(j + 1) * block_width] = squareList[i * degree + j]
            compare = cv2.subtract(canva, copy_image)
            result = not np.any(compare)
            print(result)
            if result is True:
                current_time = time.monotonic()
                spend_time = current_time - start_time
                print(f"start: {start_time}s, end: {current_time}s")
                print(f"total: {spend_time}s")
                cv2.rectangle(canva, (150, 150), (550, 550), (215, 203, 193), -1)
                cv2.putText(canva, "Success!", (205, 300), cv2.FONT_HERSHEY_TRIPLEX, 2, (169, 150, 134), 1)
                cv2.putText(canva, f"step = {step}", (280, 350), cv2.FONT_HERSHEY_TRIPLEX, 1, (169, 150, 134), 1)
                cv2.putText(canva, f"time = {spend_time:.5f}s", (205, 400), cv2.FONT_HERSHEY_TRIPLEX, 1, (169, 150, 134), 1)
                cv2.rectangle(canva, (200, 480), (350, 520), (184, 168, 156), -1)
                cv2.putText(canva, "Play again", (210, 510), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                cv2.rectangle(canva, (400, 480), (500, 520), (184, 168, 156), -1)
                cv2.putText(canva, "Leave", (415, 510), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                cv2.setMouseCallback('Game!', reset_game)
        if 570 <= x <= 670 and 10 <= y <= 50:
            canva = cv2.imread("background.jpg")
            cv2.putText(canva, "PUZZLE GAME!", (157, 150), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 0), 2)
            cv2.rectangle(canva, (320, 190), (480, 240), (0, 240, 204), -1)
            cv2.putText(canva, "Select", (355, 225), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.rectangle(canva, (320, 270), (480, 320), (0, 230, 140), -1)
            cv2.putText(canva, "Start", (360, 305), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.setMouseCallback('Game!', button_click)
            reset_base()
            return
    current_time = time.monotonic()
    spend_time = current_time - start_time
    cv2.rectangle(canva, (570, 10), (670, 50), (159, 181, 162), -1)
    cv2.putText(canva, "BACK", (585, 35), cv2.FONT_HERSHEY_TRIPLEX, 0.8, (255, 255, 255), 1)
    cv2.putText(canva, f"step = {step}", (35, 600), cv2.FONT_HERSHEY_TRIPLEX, 0.8, (255, 255, 255), 1)
    


# 分割圖片
def split_picture(image):
    global degree
    global canva
    global height
    global width
    global c
    global block_height
    global block_width
    global copy_image
    height, width, c = image.shape[:3]
    block_height = height // degree
    block_width = width // degree
    # ------------將圖片切成n*n------------
    for i in range(degree):
        for j in range(degree):
            square = image[i * block_height:(i + 1) * block_height, j * block_width:(j + 1) * block_width]
            squareList.append(square)          # 將切下來的square添加到列表的末尾。
    random.shuffle(squareList)
    canva = np.zeros((height, width, c), np.uint8)
    for i in range(degree):
        for j in range(degree):
            canva[i * block_height:(i + 1) * block_height, j * block_width:(j + 1) * block_width] = squareList[i * degree + j]
    copy_image = image.copy()


# 開始遊戲介面
def game_start(event, x, y, flags, param):
    global canva
    global squareList
    global firstClick
    if event == cv2.EVENT_LBUTTONDOWN:
        if 570 <= x <= 670 and 10 <= y <= 50:
            canva = cv2.imread("background.jpg")
            cv2.putText(canva, "PUZZLE GAME!", (157, 150), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 0), 2)
            cv2.rectangle(canva, (320, 190), (480, 240), (0, 240, 204), -1)
            cv2.putText(canva, "Select", (355, 225), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.rectangle(canva, (320, 270), (480, 320), (0, 230, 140), -1)
            cv2.putText(canva, "Start", (360, 305), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            reset_base()
            cv2.setMouseCallback('Game!', button_click)


# 起始介面
cv2.putText(canva, "PUZZLE GAME!", (157, 150), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 0), 2)
cv2.rectangle(canva, (320, 190), (480, 240), (0, 240, 204), -1)
cv2.putText(canva, "Select", (355, 225), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
cv2.rectangle(canva, (320, 270), (480, 320), (0, 230, 140), -1)
cv2.putText(canva, "Start", (360, 305), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
cv2.namedWindow('Game!')
cv2.setMouseCallback('Game!', button_click)

while True:
    cv2.imshow("Game!", canva)
    if degree == 3:
        remain_time = count_time - spend_time
        cv2.putText(canva, f"time = {remain_time:.2f}", (35, 630), cv2.FONT_HERSHEY_TRIPLEX, 0.8, (255, 255, 255), 1)
        if remain_time <= 0:
            cv2.rectangle(canva, (150, 150), (550, 550), (215, 203, 193), -1)
            cv2.putText(canva, "Times up!", (230, 300), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (169, 150, 134), 1)
            cv2.putText(canva, "Game Over!", (200, 350), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (169, 150, 134), 1)
            cv2.rectangle(canva, (200, 480), (350, 520), (184, 168, 156), -1)
            cv2.putText(canva, "Play again", (210, 510), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.rectangle(canva, (400, 480), (500, 520), (184, 168, 156), -1)
            cv2.putText(canva, "Leave", (415, 510), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.setMouseCallback('Game!', reset_game)
    elif degree == 4 or degree == 5:
        cv2.putText(canva, f"time = {spend_time:.2f}", (35, 630), cv2.FONT_HERSHEY_TRIPLEX, 0.8, (255, 255, 255), 1)
    if (cv2.waitKey(1) & 0xFF == 27) or end_game is True:
        break

cv2.destroyAllWindows()
