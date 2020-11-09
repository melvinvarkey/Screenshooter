#!/usr/bin/env python3
#!/usr/bin/env python3
'''
  ██████  ▄████▄   ██▀███  ▓█████ ▓█████  ███▄    █   ██████  ██░ ██  ▒█████   ▒█████  ▄▄▄█████▓▓█████  ██▀███  
▒██    ▒ ▒██▀ ▀█  ▓██ ▒ ██▒▓█   ▀ ▓█   ▀  ██ ▀█   █ ▒██    ▒ ▓██░ ██▒▒██▒  ██▒▒██▒  ██▒▓  ██▒ ▓▒▓█   ▀ ▓██ ▒ ██▒
░ ▓██▄   ▒▓█    ▄ ▓██ ░▄█ ▒▒███   ▒███   ▓██  ▀█ ██▒░ ▓██▄   ▒██▀▀██░▒██░  ██▒▒██░  ██▒▒ ▓██░ ▒░▒███   ▓██ ░▄█ ▒
  ▒   ██▒▒▓▓▄ ▄██▒▒██▀▀█▄  ▒▓█  ▄ ▒▓█  ▄ ▓██▒  ▐▌██▒  ▒   ██▒░▓█ ░██ ▒██   ██░▒██   ██░░ ▓██▓ ░ ▒▓█  ▄ ▒██▀▀█▄  
▒██████▒▒▒ ▓███▀ ░░██▓ ▒██▒░▒████▒░▒████▒▒██░   ▓██░▒██████▒▒░▓█▒░██▓░ ████▓▒░░ ████▓▒░  ▒██▒ ░ ░▒████▒░██▓ ▒██▒
▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░ ▒▓ ░▒▓░░░ ▒░ ░░░ ▒░ ░░ ▒░   ▒ ▒ ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░ ▒░▒░▒░ ░ ▒░▒░▒░   ▒ ░░   ░░ ▒░ ░░ ▒▓ ░▒▓░
░ ░▒  ░ ░  ░  ▒     ░▒ ░ ▒░ ░ ░  ░ ░ ░  ░░ ░░   ░ ▒░░ ░▒  ░ ░ ▒ ░▒░ ░  ░ ▒ ▒░   ░ ▒ ▒░     ░     ░ ░  ░  ░▒ ░ ▒░
░  ░  ░  ░          ░░   ░    ░      ░      ░   ░ ░ ░  ░  ░   ░  ░░ ░░ ░ ░ ▒  ░ ░ ░ ▒    ░         ░     ░░   ░ 
      ░  ░ ░         ░        ░  ░   ░  ░         ░       ░   ░  ░  ░    ░ ░      ░ ░              ░  ░   ░     
         ░                                                                                                      
'''
import pyautogui
import time
import webbrowser
import tempfile
import requests as req
import argparse
import re
import time
import logging
from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Install chromedriver from https://sites.google.com/a/chromium.org/chromedriver/downloads
# chrome_options = Options()
# chrome_options.add_argument('--no-startup-window')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')

CHROME_PATH = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
CHROMEDRIVER_PATH = 'C:\\chromedriver_win32\\chromedriver.exe'
WINDOW_SIZE = "1920,1080"

chrome_options = webdriver.ChromeOptions()  
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.add_argument("--log-level=OFF")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')


# Sometimes, selenium randomly crashed when using seleniumwire, these options fixed that.
# Probably has to do with how it proxies everything.
# https://stackoverflow.com/questions/17361742/download-image-with-selenium-python

chrome_options.binary_location = CHROME_PATH

#Selenium driver code
#driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,chrome_options=chrome_options)  
driver.maximize_window()

parser = argparse.ArgumentParser(description='Automate the process of visually validate targets based on the landing page by going through the screenshots')
parser.add_argument('-t', '--targets', help='File contains all the target domains')
parser.add_argument('-S', '--sleep', help='Sleep time (default=5sec)')

# TODO Stuff
# parser.add_argument('-o', '--output', help='Output screenshots to the specified folder')
# parser.add_argument('-e', '--extension', help='(In development) Specify the output format')
# parser.add_argument('-s', '--size', help='(In development) Specify the size of the screenshot')
# parser.add_argument('-T', '--Threads', help='(In development) Specify the size of the screenshot')

args = parser.parse_args()

def sleeperFunction():
    if args.sleep is not None:
            time.sleep(args.sleep)
    else:
        time.sleep(10)

def screenshooter(URI):
    try:
        driver.get(URI)
        tf = tempfile.NamedTemporaryFile()
        print(URI)
        imgName = URI + tf.name + ".png"
        print(imgName)
        print("[+] Screenshot Successful")
        print("URL: {0} | Stored: {1}\n".format(URI, imgName))
        driver.save_screenshot(imgName)

    except:
        print("[+] Error in URI format (expected HTTP / HTTPS)")

    else:
        sleeperFunction()
        
def main():
    if args.targets is not None:
        with open(args.targets) as targetUrl:
            for targetName in targetUrl:
                screenshooter(targetName)

if __name__ == "__main__":
    main()
    driver.close()
    driver.quit()