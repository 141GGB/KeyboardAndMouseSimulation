import enum

import colorama
import pyfiglet
import pyfiglet.fonts
import pynput
from pynput.mouse import Controller,Button,Listener
from pynput import keyboard
import time
import os
import pickle
import threading
from colorama import Fore,Style
colorama.init(autoreset=True)

mouse = Controller()

listOfOrder = []
Start = True
listenStart = False
FristEnter = False
CWD = os.getcwd()
FileSaveName = ""
LOOP = False

specialEvent = {
    "space": pynput.keyboard.Key.space,
    "ctrl":pynput.keyboard.Key.ctrl,
    "shift":pynput.keyboard.Key.shift,
    "alt":pynput.keyboard.Key.alt,
}
if (not 'Scirpts' in os.listdir(CWD)):
    os.mkdir("Scirpts")

#记录键鼠事件并保存文本
def RecordEvent():
    global FileSaveName
    print(Fore.RED+"需要退出请输入'quit'")
    FileSaveName = input(Fore.GREEN+"请提前输入文件名:")
    if FileSaveName == "quit":
        return False
    loop = input(Fore.GREEN + "是否循环该脚本(请输入y或者n):")
    if loop == 'y':
        LOOP = True
    elif loop == 'n':
        LOOP = False
    else:
        print("输入错误。将默认为n")
        LOOP = False
    print(Fore.GREEN+"按下F10开始记录键鼠，按下F9停止记录")

    def on_click(x,y,button,pressed):
        global listenStart
        if (pressed and listenStart):
            mouseEvent = {
                    "Btn":button,
                    "x":x,
                    "y":y,
                }
            listOfOrder.append(mouseEvent)
            print(Fore.GREEN+"位于:{0},{1},按下了{2}".format(x,y,button))
            
        elif (listenStart and not pressed):
            listOfOrder.append("mouseFree")
            print(Fore.GREEN+"释放了{0}按键".format(button))
            
            

    def on_press(key):
        global listenStart,FristEnter
        FristEnter = False
        if (key == keyboard.Key.f9):
                listenStart = False

                print(Fore.GREEN+"--记录结束--")
                if (len(listOfOrder) <= 0):
                    print(Fore.GREEN+"没做任何操作")
                else:

                    listOfOrder.append(LOOP)
                    with open(f"{CWD}\\Scirpts\\{FileSaveName}.txt", "wb") as f:
                        pickle.dump(listOfOrder, f)
                    print(Fore.GREEN + "脚本写入成功")
                    return False


        if (not listenStart):
            if (key == keyboard.Key.f10):
                FristEnter = True
                listenStart = True
                print(Fore.GREEN+"--开始记录--")
                return
        if (listenStart):
            listOfOrder.append(key)
            print(Fore.GREEN+"{0}已按下".format(key))

    def on_release(key):
        global listenStart,FristEntern
        if (FristEnter):
            return
        if (listenStart):
            listOfOrder.append("KeyFree")
            print(Fore.GREEN+'{0}已释放'.format(key))

    mouse_listener = Listener(on_click=on_click)
    mouse_listener.start()


    with keyboard.Listener(
        on_press = on_press,
        on_release = on_release
        ) as KListener:
        KListener.join()

Status = True

def listen_quit(key):
    global Status
    if key == keyboard.Key.f9:
        print(Fore.GREEN+"----脚本运行结束----")
        Status = False

def ListenKeyBB():
    with keyboard.Listener(
            on_press=listen_quit
    ) as KListener:
        KListener.join()

def RunEvent():
    global Status,stopListen

    if "Scirpts" in os.listdir("./"):
        if len(os.listdir("./Scirpts")) != 0:
            while True:
                print(Fore.GREEN+"你的脚本:\n"+str(os.listdir("./Scirpts")))
                print(Fore.BLUE+"退出请输入'quit'")
                scriptName = input(Fore.GREEN+"请选择脚本(输入名称和后缀名):")
                if scriptName == "quit":
                    return False
                if scriptName in os.listdir("./Scirpts"):
                    Status = True
                    with open(f"./Scirpts/{scriptName}", "rb") as f:
                        script = pickle.load(f)
                        break
                else:
                    print(Fore.RED+"文件不存在")
                    continue
        else:
            print(Fore.RED+"你还没有创建脚本")
            return False
        Mousectr = pynput.mouse.Controller()
        Keyctr = pynput.keyboard.Controller()
    else:
        print(Fore.RED+"你还没有创建脚本")
        return False


    while Status:
        for event in script:

            if not script[-1]:
                break

            time.sleep(0.1)

            if type(event) == dict:

                Mousectr.position = (event['x'], event['y'])

                Mousectr.click(event["Btn"])

                needMRelease = event["Btn"]

            elif event == "mouseFree":

                Mousectr.release(needMRelease)

            elif type(event) == pynput.keyboard.KeyCode:

                Keyctr.press(event)

                needKRelease = event

            elif event == "KeyFree":

                print(Fore.GREEN + f"{needKRelease}已释放")

                if isinstance(event, enum.Enum):
                    Keyctr.release(specialEvent[str(needKRelease).split(".")])

                    return 0

                Keyctr.release(needKRelease)

            elif isinstance(event, enum.Enum):  # isinstance(value,enum.Enum)判断是否为枚举

                eventName = str(event).split(".")[1]

                specialEvent[eventName]

                needKRelease = event
            elif type(event) == bool:
                if event:
                    print(Fore.GREEN+"----继续循环----")
                else:
                    print(Fore.GREEN+"----结束----")
            else:

                print(Fore.GREEN + f"{event}:{type(event)}")


#开始菜单
def main():
    print(Style.BRIGHT+Fore.GREEN+"这里是键鼠模拟脚本")

    print(Fore.GREEN+"温馨提醒本脚本还在测试阶段BUG很多\t"
          "版本:0.002\n"
          "可能会添加如下内容:自定义文字颜色、自定义映射结束按键......\n"
          "当然只是可能\n"
          "已知BUG进入运行脚本后不能返回上一级----已解决----")
    print(Fore.GREEN+Style.BRIGHT+"版权拥有者:")
    f = pyfiglet.Figlet()
    print(Fore.GREEN+f.renderText("1 4 1 G G B"))

    while True:
        option = input(Fore.GREEN + "1、创建脚本\n2、运行脚本\n3、退出程序\n请输入你的选择(1,2,3):")

        if option == '1':
            RecordEvent()
        elif option == '2':
            t1 = threading.Thread(target=ListenKeyBB)
            t1.daemon = True
            t1.start()
            RunEvent()

        elif option == '3':
            break

if __name__ == '__main__':
    main()

    print(Fore.GREEN+"程序结束")

