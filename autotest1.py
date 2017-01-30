import subprocess
import sys
import time
import os
import re
from pywinauto import application
from datetime import datetime, timedelta

PATH_TO_KIS_LAUNCHER = r"C:\Program Files (x86)\Kaspersky Lab\Kaspersky Internet Security 17.0.0\avpui.exe"
PATH_TO_KIS_CMD_UI = r"C:\Program Files (x86)\Kaspersky Lab\Kaspersky Internet Security 17.0.0\avp.com"
PATH_TO_IE = r"C:\Program Files\Internet Explorer\iexplore.exe"
FOLDER_TO_SAVE = r"C:\Users\Sir Nightmare\PycharmProjects\autotests"
SAVED_PAGE_NAME = "antiphishing_test.html"
REPORT_FILE_NAME = "report.csv"
REASON_TO_BLOCK = "phishing URL"
KIS_PASSWORD = "Insert_your_password_here"


def get_url():
    if len(sys.argv) == 2:
        return sys.argv[1]
    else:
        print('You need to input correct url')
        sys.exit()


def turn_on_protection(kis_launcher, kis_cmd):
    subprocess.Popen(kis_launcher)
    subprocess.Popen([kis_cmd, "start", "Web_Monitoring"], shell=True)


def kill_ie(ie_path):
    '''
    If there are several IE windows openen, pywinauto cannot connect with proper window correctly
    to save Internet page
    '''

    ie_works = True
    while ie_works:
        try:
            exp = application.Application().connect(path=ie_path)
            exp.kill()
        except application.ProcessNotFoundError:
            ie_works = False


def clear_ie_files():
    '''
    Sometimes the banner is not shown on the phishing page. This situation might occur after opening
    the same phishing url many times.
    Clearing the history, cookies and temp files helped.
    '''
    subprocess.Popen([r"RunDll32.exe", "InetCpl.cpl,ClearMyTracksByProcess", "1"], shell=True)
    subprocess.Popen([r"RunDll32.exe", "InetCpl.cpl,ClearMyTracksByProcess", "2"], shell=True)
    subprocess.Popen([r"RunDll32.exe", "InetCpl.cpl,ClearMyTracksByProcess", "8"], shell=True)


def save_web_page(path_to_ie, web_address, folder_to_save, saved_page_name):
    '''
    :return: time of blocking
    '''
    filepath = os.path.join(folder_to_save, saved_page_name)
    if os.path.exists(filepath):
        os.unlink(filepath)
    app = application.Application().start(path_to_ie + " %s" % web_address)
    time_of_blocking = datetime.today()
    time.sleep(2)
    ie = app.window_()
    ie.TypeKeys("%")
    ie.TypeKeys("F")  # Sometimes IE does not get all symbols sent together when Russian keyboard
    ie.TypeKeys("A")  # layout is on. So the symbols are sent separately
    app.SaveWebPage.Edit.SetEditText(filepath)
    app.SaveWebPage.Save.CloseClick()
    time.sleep(1)
    ie.TypeKeys("%")
    ie.TypeKeys("F")
    ie.TypeKeys("C")
    return time_of_blocking


def is_kis_banner(folder_to_save, saved_page_name, reason_to_block, web_address):
    color1 = r"background: rgb\(227, 54, 48\)"
    color2 = r"background: rgb\(191, 10, 10\)"
    url = r'title=3D"{}"'.format(web_address)
    reason = r"Reason: phishing URL"
    filepath = os.path.join(folder_to_save, saved_page_name)
    with open(filepath, 'r') as web_page_file:
        web_page = web_page_file.read()
        is_color1 = re.search(color1, web_page)
        is_color2 = re.search(color2, web_page)
        is_url = re.search(url, web_page)
        is_reason = re.search(reason, web_page)
        return is_color1 and is_color2 and is_url and is_reason


def check_report(kis_cmd, folder_to_save, report_file_name, time_of_blocking, web_address):
    filepath = os.path.join(folder_to_save, report_file_name)
    subprocess.Popen([kis_cmd, "REPORT", "Web_Monitoring", "/RA:" + filepath],
                     shell=True)
    time.sleep(1)
    with open(filepath, 'r') as report:
        for line in report:
            info = line.split(';')
            if len(info[0]) < 16:
                continue
            record_time = datetime.strptime(info[0], "%d.%m.%Y %H.%M.%S")
            if timedelta(seconds=-2) < time_of_blocking - record_time < timedelta(seconds=2):
                if web_address in info:
                    return True
            if time_of_blocking - record_time > timedelta(seconds=10):
                return


def turn_off_protection(kis_cmd, password):
    subprocess.Popen(
        [kis_cmd, "stop", "Web_Monitoring", "/password=" + password], shell=True)
    subprocess.Popen(
        [kis_cmd, "EXIT", "/password=" + password], shell=True)


if __name__ == '__main__':
    url_to_check = get_url()
    turn_on_protection(PATH_TO_KIS_LAUNCHER, PATH_TO_KIS_CMD_UI)
    time.sleep(10)
    kill_ie(PATH_TO_IE)
    clear_ie_files()
    time.sleep(3)
    time_of_blocking = save_web_page(PATH_TO_IE, url_to_check, FOLDER_TO_SAVE, SAVED_PAGE_NAME)
    if is_kis_banner(FOLDER_TO_SAVE, SAVED_PAGE_NAME, REASON_TO_BLOCK, url_to_check):
        print("There was the KIS banner.")
    else:
        print("There was NO KIS banner.")
    if check_report(PATH_TO_KIS_CMD_UI, FOLDER_TO_SAVE, REPORT_FILE_NAME, time_of_blocking,
                    url_to_check):
        print("There is a record about blocking the page.")
    else:
        print("There is NO record about blocking the page.")
    turn_off_protection(PATH_TO_KIS_CMD_UI, KIS_PASSWORD)
