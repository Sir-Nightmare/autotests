#Autotests for Kaspersky Internet Security ( [Safeboard Internship](http://safeboard.kaspersky.ru/) homework)

- **autotest1** checks if phishing urls are not opened and KIS banner is shown.
- **autotest2** checks if custom scan is working properly while File Antivirus is turned off.
- **autotest3** checks that screenshots are completely black while Safe Browser is working.

## Usage
- **Clone repository:** `git clone https://github.com/Sir-Nightmare/autotests.git`  
- **Install necessary modules:** `pip3 install -r requirements.txt`
- **Edit global constants with paths and password in needed script**
- **Run needed script:**   
`python autotest1.py <url to check>`   
`python autotest2.py`   
`python autotest3.py <url of a bank or PayPal enc>`   

####Notes:
- [KIS 2017](https://products.s.kaspersky-labs.com/english/homeuser/kis2017/kis17.0.0.611en_11482.exe) 
have to be installed.
- You need to set a password to managing KIS which will be used in autotests.
- Windows Defender has to be [turned off](http://www.howtogeek.com/howto/15788/how-to-uninstall-disable-and-remove-windows-defender.-also-how-turn-it-off/).
- Autotest1 will close all IE windows and clear IE history, cookies and temp files. It is essential to
guarantee proper work.

####Examples:

```
python autotest1.py http://www.kaspersky.com/antiphishing_test
python autotest2.py
python autotest3.py https://paypal.com
```

####Заметки о процессе разработки третьего автотеста

Было интересно проверить, как будут работать другие способы получения скриншота,
ведь если делать его вручную, то все корректно работает.
Через Chrome Remote Desktop видно картинку, которая была перед включением безопасного браузера
или черный экран, если безопасный браузер был включен до удаленного подключения.
Я решил попробовать эмулировать ручное получение скриншота, на StackOverflow нашел код,
написанный с помощью ctypes и передающий коды клавиатуры, однако ничего не вышло.
В буфере обмена даже черной картинки не было, туда вообще ничего не попадало. Выводилось то,
что там было до работы скрипта, при том что без запущенного безопасного браузера все работало
корректно.
Видимо это заблокировано где-то глубже и хитрее, раз ручное получение работает.
Могу предположить, что написанное выше достаточно очевидно, но хотелось проверить самому)