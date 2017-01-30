import subprocess
import time
import os
from datetime import datetime, timedelta

PATH_TO_KIS_LAUNCHER = r"C:\Program Files (x86)\Kaspersky Lab\Kaspersky Internet Security 17.0.0\avpui.exe"
PATH_TO_KIS_CMD_UI = r"C:\Program Files (x86)\Kaspersky Lab\Kaspersky Internet Security 17.0.0\avp.com"
FOLDER_TO_CHECK = r"D:\Samples\CustomScan"
FILE_TO_CHECK = r"uncurable.com"
REPORT_FILE_NAME = "report_scan.csv"
FOLDER_TO_SAVE = r"C:\Users\Sir Nightmare\PycharmProjects\autotests"
KIS_PASSWORD = "Insert_your_password_here"


def check_report(kis_cmd, folder_to_save, report_file_name, time_of_scan, filepath):
    report_path = os.path.join(folder_to_save, report_file_name)
    subprocess.Popen([kis_cmd, "REPORT", "Scan_Objects", "/RA:" + report_path],
                     shell=True)
    time.sleep(5)
    phrase_to_search = "Detected object (file) deleted"
    with open(report_path, 'r') as report:
        for line in report:
            info = line.split(';')
            if len(info[0]) < 16:
                continue
            record_time = datetime.strptime(info[0], "%d.%m.%Y %H.%M.%S")
            if timedelta(seconds=-15) < time_of_scan - record_time < timedelta(seconds=15):
                if phrase_to_search == info[1] and filepath == info[2]:
                    return True
            if time_of_scan - record_time > timedelta(seconds=40):
                return


if __name__ == '__main__':
    subprocess.Popen(PATH_TO_KIS_LAUNCHER)
    subprocess.Popen([PATH_TO_KIS_CMD_UI, "stop", "File_Monitoring", "/password=" + KIS_PASSWORD],
                     shell=True)
    time.sleep(5)
    filepath = os.path.join(FOLDER_TO_CHECK, FILE_TO_CHECK)
    subprocess.Popen([PATH_TO_KIS_CMD_UI, "scan", FOLDER_TO_CHECK], shell=True)
    time.sleep(12)
    time_of_scan = datetime.today()
    time.sleep(8)
    if not os.path.exists(filepath):
        print('File was deleted')
    else:
        print('File was not deleted')
    if check_report(PATH_TO_KIS_CMD_UI, FOLDER_TO_SAVE, REPORT_FILE_NAME, time_of_scan, filepath):
        print("There is a record about deleting the file.")
    else:
        print("There is NO record about deleting the file.")
    subprocess.Popen([PATH_TO_KIS_CMD_UI, "EXIT", "/password=" + KIS_PASSWORD], shell=True)
