# Class import
from WebScraper import WebScraper, EmailResponse

# Importing libraries
from selenium.webdriver.chrome.options import Options
from yaml import safe_load
from time import sleep
from datetime import datetime

# Opens the config file filled with all user information
with open('config.yaml', 'r') as file:
    config = safe_load(file)

# Defining the webdriver options
browser_options = Options()
browser_options.headless = True
browser_options.binary_location = config["chrome_path"]

# Initializes web scraping class, adds browser options and config contents
Securities_Agent = WebScraper(browser_options, config)

# Logging in
Securities_Agent.login()

# Runs purchases every execution, Returns # of consecutive purchases made.
Num_Successful_Purchases = Securities_Agent.regular_security_purchasing()

# Returns day of week (0=Monday, 4=Friday)
Current_Day = datetime.today().weekday()

# Day of the week checked for individual purchases.
for (security, price, day) in zip(config["individual_security_purchases"], config["individual_security_prices"], config["individual_purchase_dates"]):
    if Current_Day == day and Num_Successful_Purchases != 0:
        Num_Successful_Purchases = Securities_Agent.individual_security_purchasing(Num_Successful_Purchases, security, price)
    sleep(2)

# If the config option for EMAIL is TRUE
if config['Email']:
    # Initializes email bot class, adds webscraper object, config contents, and number of successful purchases made
    emailer = EmailResponse(Securities_Agent, config, Num_Successful_Purchases)
    
    # Returns strings used for email body 
    purchase_sum = emailer.email_purchases_creator()
    error_msg_sum = emailer.email_error_msg_creator()
    purchase_sum += error_msg_sum

    # Sends email
    emailer.email(purchase_sum)
