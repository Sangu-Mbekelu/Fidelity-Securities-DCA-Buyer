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
