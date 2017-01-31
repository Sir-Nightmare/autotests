#Autotests for Kaspersky Internet Security (Safeboard Internship homework)

-**autotest1** checks if phishing urls are not opened and KIS banner is shown.
-**autotest2** checks if custom scan is working properly while File Antivirus is turned off.
-**autotest3** checks that screenshots are completely black while Safe Browser is working.

## Usage
- **Clone repository:** `git clone https://github.com/Sir-Nightmare/autotests.git`  
- **Install necessary module _pywinauto_:** `pip3 install -r requirements.txt`
- **Edit constants with paths and password in needed script**
- **Run needed script:** 
`python autotest1.py <url to check>` 
`python autotest2.py` 
`python autotest3.py <url of a bank or PayPal enc>` 

**Note:**
- [KIS 2017](https://products.s.kaspersky-labs.com/english/homeuser/kis2017/kis17.0.0.611en_11482.exe) 
have to be installed.
- You need to set a password to managing KIS which will be used in autotests.
- Windows Defender has to be [turned off](http://www.howtogeek.com/howto/15788/how-to-uninstall-disable-and-remove-windows-defender.-also-how-turn-it-off/).

**Examples:**

```
python autotest1.py http://www.kaspersky.com/antiphishing_test
python autotest2.py
python autotest3.py https://paypal.com
```