<h1 align="center"> Fidelity Stock/ETF Purchaser </h1>

## Background
&nbsp; &nbsp; __Dollar Cost Averaging:__

- An investment strategy that relies on regularly purchasing securities <br>
for the same dollar amount regardless of the market. <br>
- A non-optimal way of mitigating non-ideal lump sum timing and investor psyche <br>
-  A common example of DCA investing is a 401k<br>

&nbsp;&nbsp; __*Why?*__

- Already had a Fidelity account
- Fidelity doesn't have a feature that allows scheduled individual stock purchases
- Little maintenance anticipated (Fidelity barely changes their site)
- Fidelity to schedule stock purchases



## Installation

### Python Version
- Python 3.9.13 only version used to test
- I believe Python 3.8+ would work out __*- not tested*__


### Config file

#### Downloading Chrome For Testing
Link used to download Chrome for Testing:
https://googlechromelabs.github.io/chrome-for-testing/  

Must download a version of chrome and include the unzipped directory path to the config
```yaml
# config.yaml
# Enter absolute path of downloaded Chrome For Testing .exe
chrome_path: "C:\\chrome_117\\chrome.exe" # example windows path to chrome.exe
```

#### Secuirties
Initial list will be purchased every time the code is executed.   
The two lists are correlated by indices and can be as long as needed:  
Buying "SPX" for $700  
Buying "INDU" for $90  
<sub>Note: Fidelity does have fractional shares, but you must buy a minimum of 0.001 shares</sub>
``` yaml
# config.yaml
security_purchases:
  - "SPX"
  - "INDU"
  - ...

security_prices:
  - "700"
  - "90"
  - ...
```
For all "individual" purchases, there is an additional value for the day of the week the security will be pruchased:  
"VOO" purchased for $370 on Wednesday only
``` yaml
# config.yaml
individual_security_purchases:
  - "VOO"
  - ...

individual_security_prices:
  - "370"
  - ...
individual_purchase_dates: # Enter day of the week (0=Monday, 4=Friday)
  - 2
  - ...
```
#### Bot Email

Guide to getting gmail app password key:  
https://support.google.com/mail/answer/185833?hl=en  

Once the key is given, the account can be used to send emails with python.  
Must use gmail, will need to modify/disable email otherwise.  

Email is set off by default in config.  
For use, change to true and add relevant information in config


### Scheduling using Windows Task Scheduler
Powershell script included to run the python script periodically through the Windows task scheduler.  
Guide to use task scheduler: https://linuxhint.com/schedule-powershell-script-using-task-scheduler   

```powershell
# DCA_Scheduler.ps1

$WorkingDirectory = "" # add working directory path

cd $WorkingDirectory

# Personally use a virtual environment, so change to suit name of venv folder
.\venv\Scripts\activate.ps1

$HolidayCheck = (Get-Content -Path .\holiday_check.txt)

if ($HolidayCheck -eq "YES"){

    python .\main.py

    "NO" | Out-File -FilePath .\holiday_check.txt

} else {

    if ( (Get-Date).DayofWeek -eq "Monday" -Or "Wednesday" -Or "Friday" ){
        python .\main.py
    }
    
}
```
Add the path to the working directory and either remove or modify the virtual environment path.

#### ------------------- *Disclaimers* -------------------

<sub>- __*THIS IS MY WORK*__<br>
<sub>- All for personal use</sub>

<sub>- __*NOT FINANCIAL ADVICE*__ <br>
-This is not an investment recommendation  <br>
<sub>- This will not guarantee profit  </sub><br>
<sub>- I'm not a financial advisor  </sub><br>
<sub>- I don't endorse Fidelity as a brokerage </sub> <br>
<sub>- There is inherent risk in all financial assets, and the stock market is a casino </sub><br>
<sub>- __*Consult the professional, certificate carrying gamblers before any new investment decisions*__ </sub></sub><br> 
