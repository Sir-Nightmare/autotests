import subprocess
import sys
import time
from PIL import ImageGrab

PATH_TO_KIS_LAUNCHER = r"C:\Program Files (x86)\Kaspersky Lab\Kaspersky Internet Security 17.0.0\avpui.exe"
PATH_TO_KIS_CMD_UI = r"C:\Program Files (x86)\Kaspersky Lab\Kaspersky Internet Security 17.0.0\avp.com"
KIS_PASSWORD = "Insert_your_password_here"


def get_url():
    if len(sys.argv) == 2:
        return sys.argv[1]
    else:
        print('You need to input correct url')
        sys.exit()


def is_black(image):
    width = image.size[0]
    height = image.size[1]
    pix = image.load()
    for i in range(height):
        for j in range(width):
            a = pix[j, i][0]
            b = pix[j, i][1]
            c = pix[j, i][2]
            if not (a == 0 and b == 0 and c == 0):
                return
    return True


if __name__ == '__main__':
    web_address = get_url()
    subprocess.Popen(PATH_TO_KIS_LAUNCHER)
    time.sleep(10)
    subprocess.Popen(r"start chrome {}".format(web_address), shell=True)
    time.sleep(10)
    img = ImageGrab.grab()
    if is_black(img):
        print("Screen image is completely black")
    else:
        print("Screen image is not black")
    subprocess.Popen([PATH_TO_KIS_CMD_UI, "EXIT", "/password=" + KIS_PASSWORD], shell=True)
