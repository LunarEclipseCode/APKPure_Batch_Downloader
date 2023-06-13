## APKPure Batch Downloader

Let's say you want to download the latest version of all apps made by a certain developer. Let's take Softecks for example. From [here](https://apkpure.com/developer/Softecks), you realize they have over 400 apps on APKPure. Now, if you want to download some/all of thsoe, then this script is for you. There are some other batch downloader for APKPure, each with their unique features. Note that I haven't tested these, and some of them haven't been updated in a while, so not sure if they still work.

[0x27/apkpure_get](https://github.com/0x27/apkpure_get): If you have a list of app packages like com.developer.app

[zackhorvath/apk_downloader](https://github.com/zackhorvath/apk_downloader): Similar to the first one but better documentation and more options like which version of the app you want to download and the download timeout.

### How to run this script:

First of course, you need Python and VS Code. You can download VS code from [here](https://code.visualstudio.com/) and Python [here](https://www.python.org/downloads/release/python-3113/) . During Python installation, make sure to click on `Add Python to PATH`. In VS code, install the Python extension too.

In VS code, you will get yellow squiggle under the import statements for Python libraries/packages that you don't have installed. Based on the squiggle lines you have, you need to run some or all these on powershell/terminal.

```python
pip install requests
pip install selenium
pip install urllib3
pip install beautifulsoup4
```

Restart VS code and the yellow squiggle should be gone. If it's still there, try View-> Command Palette -> Python: Select Interpreter and set it to the Python version.

### Note:

You might have multiple versions of Python present on your computer. Many softwares require Python to run, so they migth have installed Python during the software's installation process. You can go to Control Panel -> Programs and Features to see if you have multiple versions of Python installed. In that case, it may be unclear under which version of Python selenium has been installed. So, run `pip show Selenium`, to check under which the Python version Selenium is installed. Now, in VS code, click on `View-> Command Palette -> Python: Select Interpreter` and set it to the Python version where Selenium is installed.

Now based on whether you want to use Chrome or Firefox, set `browser` to "chrome" or "firefox". If you are using Firefox:

1. Download geckodriver from [here](https://github.com/mozilla/geckodriver/releases) and unzip the file. Copy the path to the geckodriver.exe file and paste it under `gecko_path`.

2. Finally, locate where firefox.exe is on your computer. In Windows, search for Firefox -> right click on icon and select 'Open File Location'. This will take you to the Firefox shortcut. Right click again and go to 'Open File Location.' This will take you to the actual firefox.exe loaction. Copy the path and paste it for `firefox_exe_path` variable. Please don't forget to replace `\` with `\\` when pasting path.

If you are using Chrome:

1. Download chromedriver from [here](https://github.com/mozilla/geckodriver/releases) and unzip the file. Copy the path to the chromedriver.exe file and paste it under `chrome_driver_path`.

2. Finally, locate where chrome.exe is on your computer. In Windows, search for Chrome -> right click on icon and select 'Open File Location'. This will take you to the Chrome shortcut. Right click again and go to 'Open File Location.' This will take you to the actual chrome.exe loaction. Copy the path and paste it for `chrome_exe_path` variable. Please don't forget to replace `\` with `\\` when pasting path.

Set where you want the files to be saved under `destination`. Now, for `website`, if we take the Softecks page for example, paste the link for page 1. Now mention which pages you want to download. Finally, set the number of concurrent downloads you want. I recommend keeping it at 5.

###One More Thing:

If you are using this script to download many apps, you might notice your C drive filling up. That's because in each run of the code, a temporary folder is created and over many runs, it could accumulate to something significant. To clean up these files, go to the run command and enter `%temp%`. This will open where all temporary files are saved. Just delete all of them and then delete them from Recycle Bin.

## FAQ

### Why does the code take so long?

In an ideal world, the code would have been much faster. But for some corner cases, I had to implement extra checks in the code. For example, [here](https://apkpure.com/developer/NetEase%20Games) you will see the game Fortcraft's download link just redirects to the game Creative Destruction and there is no download link available for Fortcraft. Some apps like [Minecraft Chinese Edition](https://apkpure.com/minecraft-china-edition/com.netease.x19) doesn't even have a download button. One other subtle thing is app's name contain colon and other special characters that are not allowed in the file name of Windows. All these processing take a while and so the code feels slow.

### Final Note:

Even though I did some testing, I am pretty sure there are apk files that the script cannot download for some corner case I missed. Moreover, subtle changes in the website might break the code. I will check once in couple of months to see if the code still works and update accordingly. Menawhile, if something doesn't work, please let me know.
