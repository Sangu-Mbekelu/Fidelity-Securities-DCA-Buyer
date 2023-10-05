# Importing packages
import logging

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException  # Could potentially also use NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import ActionChains

import undetected_chromedriver as uc
from time import sleep
from datetime import datetime
from logging import basicConfig, exception, debug
from email.message import EmailMessage
import ssl
import smtplib

basicConfig(filename="errorLog",
            filemode='a',
            format='%(asctime)s - %(message)s',
            datefmt='%d-%b-%y %H:%M:%S',
            level=logging.DEBUG)


class WebScraper:
    def __init__(self, browser_options, usr_config):
        self.driver = uc.Chrome(options=browser_options)
        self.action = ActionChains(self.driver)
        self.config = usr_config
        self.error_msg = ''
        self.account_balance = '0.00'
        self.working_balance = '0.00'
        self.time_purchased = []
        self.ERR = 0

    def login(self):
        # Initially getting this url to pick up cookies
        self.driver.get('https://www.fidelity.com/')

        sleep(2)  # WAIT ON HOME PAGE

        # Go to login page
        self.driver.get('https://digital.fidelity.com/prgw/digital/login/full-page')

        try:
            # Waits for username form, selects form, enters username
            WebDriverWait(self.driver, timeout=30).until(ec.element_to_be_clickable((By.ID, 'dom-username-input')))
            # Enter Username
            username_input_element = self.driver.find_element(by=By.ID, value="dom-username-input")
            username_input_element.click()
            username_input_element.send_keys(self.config['username'])
        except TimeoutException:
            self.error_msg = 'Could Not Log In'
            exception(self.error_msg)
            self.driver.close()
            return
        # Selects password form, enters password
        password_input_element = self.driver.find_element(by=By.ID, value="dom-pswd-input")
        password_input_element.click()
        password_input_element.send_keys(self.config['password'])
        # Send Enter After Password
        password_input_element.send_keys(Keys.ENTER)
        sleep(5)  # Wait for login to happen

    def regular_security_purchasing(self):
        num_purchases = 0

        # Go to 'trade' page
        self.driver.get('https://digital.fidelity.com/ftgw/digital/trade-equity/index/orderEntry')

        for num_purchases in range(0, len(self.config['security_purchases'])):
            # Default Tade Option is 'Stocks/ETFs'

            # Selecting an Account
            try:
                WebDriverWait(self.driver, timeout=30).until(ec.presence_of_element_located((By.XPATH, '//*[@id="dest-acct-dropdown"]')))
                self.driver.find_element(by=By.XPATH, value='//*[@id="dest-acct-dropdown"]').click()
                # Using a profile with only 1 account opened
                self.driver.find_element(by=By.ID, value='ett-acct-sel-list').click()
            except TimeoutException:
                self.error_msg = 'Could Not Find An Account on purchase #' + str(num_purchases + 1)
                exception(self.error_msg)
                self.ERR = 1
                self.driver.close()
                return num_purchases

            # Finding Account Balance
            # Giving to collect the real time data once and subtract from
            if num_purchases == 0:
                WebDriverWait(self.driver, timeout=30).until(
                    ec.presence_of_element_located((By.XPATH, '//*[@id="eq-ticket__account-balance"]')))
                try:
                    self.driver.find_element(by=By.XPATH, value='//*[@id="eq-ticket__account-balance"]/div[2]').is_displayed()
                    accbal = 0
                except NoSuchElementException:
                    accbal = 1

                try:
                    if accbal == 0:
                        self.account_balance = self.driver.find_element(by=By.XPATH, value='//*[@id="eq-ticket__account-balance"]/div[1]/div[2]').text
                    else:
                        self.account_balance = self.driver.find_element(by=By.XPATH, value='//*[@id="eq-ticket__account-balance"]/div/div[2]/span').text

                    self.working_balance = float(self.account_balance[1:])  # Omitting the $ in the front of the text to convert string to a float
                except TimeoutException:
                    self.error_msg = 'Could Not Find an Account Balance on purchase #' + str(num_purchases + 1)
                    exception(self.error_msg)
                    self.ERR = 1
                    self.driver.close()
                    return num_purchases

            try:
                WebDriverWait(self.driver, timeout=30).until(ec.element_to_be_clickable((By.ID, 'eq-ticket-dest-symbol')))
                etf_selector_selector = self.driver.find_element(by=By.ID, value='eq-ticket-dest-symbol')
                etf_selector_selector.click()
                etf_selector_selector.send_keys(self.config['security_purchases'][num_purchases])
                etf_selector_selector.send_keys(Keys.ENTER)
            except TimeoutException:
                self.error_msg = 'Could Not Select an ETF to buy Button on purchase #' + str(num_purchases + 1)
                exception(self.error_msg)
                self.ERR = 1
                self.driver.close()
                return num_purchases

            # Buy button
            try:
                WebDriverWait(self.driver, timeout=30).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="action-buy"]/s-root/div/label')))
                self.driver.find_element(by=By.XPATH, value='//*[@id="action-buy"]/s-root/div/label').click()
            except TimeoutException:
                self.error_msg = 'Could Not Find Buy Button on purchase #' + str(num_purchases + 1)
                exception(self.error_msg)
                self.ERR = 1
                self.driver.close()
                return num_purchases

            # Dollars button
            try:
                WebDriverWait(self.driver, timeout=30).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="quantity-type-dollars"]/s-root/div/label')))
                self.driver.find_element(by=By.XPATH, value='//*[@id="quantity-type-dollars"]/s-root/div/label').click()
            except TimeoutException:
                self.error_msg = 'Could Not Find Dollars Button on purchase #' + str(num_purchases + 1)
                exception(self.error_msg)
                self.ERR = 1
                self.driver.close()
                return num_purchases

            # Market button
            try:
                WebDriverWait(self.driver, timeout=30).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="market-yes"]/s-root/div/label')))
                self.driver.find_element(by=By.XPATH, value='//*[@id="market-yes"]/s-root/div/label').click()
            except TimeoutException:
                self.error_msg = 'Could Not Find Dollars Button on purchase #' + str(num_purchases + 1)
                exception(self.error_msg)
                self.ERR = 1
                self.driver.close()
                return num_purchases

            # If statement to ensure that there is enough cash to make the next investment. If not, break from for loop
            next_investment = float(self.config['security_prices'][num_purchases])
            if next_investment > self.working_balance:
                self.ERR = 1
                self.error_msg = 'Insufficient Funds on purchase #' + str(num_purchases + 1)
                debug(self.error_msg)
                return num_purchases
            else:
                self.working_balance -= next_investment

            # Dollar Amount Input
            try:
                WebDriverWait(self.driver, timeout=30).until(ec.element_to_be_clickable((By.ID, 'eqt-shared-quantity')))
                dollar_amount = self.driver.find_element(by=By.ID, value='eqt-shared-quantity')
                dollar_amount.send_keys(self.config['security_prices'][num_purchases])
            except TimeoutException:
                self.error_msg = 'Could Not Enter A Dollar Amount on purchase #' + str(num_purchases + 1)
                exception(self.error_msg)
                self.ERR = 1
                self.driver.close()
                return num_purchases

            # Preview Order Button
            try:
                WebDriverWait(self.driver, timeout=30).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="previewOrderBtn"]')))
                preview_order_button = self.driver.find_element(by=By.XPATH, value='//*[@id="previewOrderBtn"]')
                self.action.double_click(on_element=preview_order_button).perform()
            except TimeoutException:
                self.error_msg = 'Could Not Find Preview Order Button on purchase #' + str(num_purchases + 1)
                exception(self.error_msg)
                self.ERR = 1
                self.driver.close()
                return num_purchases

            # Place Order Button
            try:
                WebDriverWait(self.driver, timeout=30).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="placeOrderBtn"]')))
                self.driver.find_element(by=By.XPATH, value='//*[@id="placeOrderBtn"]').click()
            except TimeoutException:
                WebDriverWait(self.driver, timeout=30).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="previewOrderBtn"]')))
                try:
                    self.action.double_click(on_element=preview_order_button).perform()  # If this fails, it is more than likely a holiday and the market is closed
                except NoSuchElementException:
                    self.error_msg = "Market is Closed"
                    self.ERR = 1
                    debug(self.error_msg)
                    with open("holiday_check.txt", "w") as f:
                        f.write("YES")
                    return 0

                WebDriverWait(self.driver, timeout=30).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="placeOrderBtn"]')))
                self.driver.find_element(by=By.XPATH, value='//*[@id="placeOrderBtn"]').click()
            except:
                self.error_msg = 'Could Not Find Place Order Button on purchase #' + str(num_purchases + 1)
                exception(self.error_msg)
                self.ERR = 1
                self.driver.close()
                return num_purchases

            # Date and Time the "Place Order" Button is pressed
            self.time_purchased.append(datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            # If statement determining whether to continue to the next investment purchase or not
            if num_purchases != (len(self.config['security_purchases']) - 1):
                # New Order Button
                try:
                    WebDriverWait(self.driver, timeout=30).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="eq-ticket__enter-new-order"]')))
                    self.driver.find_element(by=By.XPATH, value='//*[@id="eq-ticket__enter-new-order"]').click()
                except TimeoutException:
                    self.error_msg = 'Could Not Find New Order Button on purchase #' + str(num_purchases + 1)
                    exception(self.error_msg)
                    self.ERR = 1
                    self.driver.close()
                    return num_purchases

        return num_purchases

    def individual_security_purchasing(self, num_purchases, security, price):
        # Go to 'trade' page
        self.driver.get('https://digital.fidelity.com/ftgw/digital/trade-equity/index/orderEntry')

        # Used to indicate a fourth purchase
        num_purchases += 1

        # Selecting an Account
        try:
            WebDriverWait(self.driver, timeout=30).until(
                ec.presence_of_element_located((By.XPATH, '//*[@id="dest-acct-dropdown"]')))
            self.driver.find_element(by=By.XPATH, value='//*[@id="dest-acct-dropdown"]').click()
            # Using a profile with only 1 account opened
            self.driver.find_element(by=By.ID, value='ett-acct-sel-list').click()
        except TimeoutException:
            self.error_msg = 'Could Not Find An Account on purchase #' + str(num_purchases + 1)
            exception(self.error_msg)
            self.ERR = 1
            self.driver.close()
            return num_purchases

        try:
            WebDriverWait(self.driver, timeout=30).until(ec.element_to_be_clickable((By.ID, 'eq-ticket-dest-symbol')))
            etf_selector_selector = self.driver.find_element(by=By.ID, value='eq-ticket-dest-symbol')
            etf_selector_selector.click()
            etf_selector_selector.send_keys(security)
            etf_selector_selector.send_keys(Keys.ENTER)
        except TimeoutException:
            self.error_msg = 'Could Not Select an ETF to buy Button on purchase #' + str(num_purchases + 1)
            exception(self.error_msg)
            self.ERR = 1
            self.driver.close()
            return num_purchases

        # Buy button
        try:
            WebDriverWait(self.driver, timeout=30).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="action-buy"]/s-root/div/label')))
            self.driver.find_element(by=By.XPATH, value='//*[@id="action-buy"]/s-root/div/label').click()
        except TimeoutException:
            self.error_msg = 'Could Not Find Buy Button on purchase #' + str(num_purchases + 1)
            exception(self.error_msg)
            self.ERR = 1
            self.driver.close()
            return num_purchases

        # Dollars button
        try:
            WebDriverWait(self.driver, timeout=30).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="quantity-type-dollars"]/s-root/div/label')))
            self.driver.find_element(by=By.XPATH, value='//*[@id="quantity-type-dollars"]/s-root/div/label').click()
        except TimeoutException:
            self.error_msg = 'Could Not Find Dollars Button on purchase #' + str(num_purchases + 1)
            exception(self.error_msg)
            self.ERR = 1
            self.driver.close()
            return num_purchases

        # Market button
        try:
            WebDriverWait(self.driver, timeout=30).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="market-yes"]/s-root/div/label')))
            self.driver.find_element(by=By.XPATH, value='//*[@id="market-yes"]/s-root/div/label').click()
        except TimeoutException:
            self.error_msg = 'Could Not Find Dollars Button on purchase #' + str(num_purchases + 1)
            exception(self.error_msg)
            self.ERR = 1
            self.driver.close()
            return num_purchases

        # If statement to ensure that there is enough cash to make the next investment. If not, break from for loop
        next_investment = float(price)
        if next_investment > float(self.working_balance):
            self.ERR = 1
            self.error_msg = 'Insufficient Funds for purchase #' + str(num_purchases + 1)
            debug(self.error_msg)
            return num_purchases
        else:
            self.working_balance -= next_investment

        # Dollar Amount Input
        try:
            WebDriverWait(self.driver, timeout=30).until(ec.element_to_be_clickable((By.ID, 'eqt-shared-quantity')))
            dollar_amount = self.driver.find_element(by=By.ID, value='eqt-shared-quantity')
            dollar_amount.send_keys(price)
        except TimeoutException:
            self.error_msg = 'Could Not Enter A Dollar Amount on purchase #' + str(num_purchases + 1)
            exception(self.error_msg)
            self.ERR = 1
            self.driver.close()
            return num_purchases

        # Preview Order Button
        try:
            WebDriverWait(self.driver, timeout=30).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="previewOrderBtn"]')))
            preview_order_button = self.driver.find_element(by=By.XPATH, value='//*[@id="previewOrderBtn"]')
            self.action.double_click(on_element=preview_order_button).perform()
        except TimeoutException:
            self.error_msg = 'Could Not Find Preview Order Button on purchase #' + str(num_purchases + 1)
            exception(self.error_msg)
            self.ERR = 1
            self.driver.close()
            return num_purchases

        # Place Order Button
        try:
            WebDriverWait(self.driver, timeout=30).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="placeOrderBtn"]')))
            self.driver.find_element(by=By.XPATH, value='//*[@id="placeOrderBtn"]').click()
        except TimeoutException:
            WebDriverWait(self.driver, timeout=30).until(
                ec.element_to_be_clickable((By.XPATH, '//*[@id="previewOrderBtn"]')))
            self.action.double_click(on_element=preview_order_button).perform()
            WebDriverWait(self.driver, timeout=30).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="placeOrderBtn"]')))
            self.driver.find_element(by=By.XPATH, value='//*[@id="placeOrderBtn"]').click()
        except:
            self.error_msg = 'Could Not Find Place Order Button on purchase #' + str(num_purchases + 1)
            exception(self.error_msg)
            self.ERR = 1
            self.driver.close()
            return num_purchases

        # Date and Time the "Place Order" Button is pressed
        self.time_purchased.append(datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

        return num_purchases


class EmailResponse:
    def __init__(self, webscraper, usr_config, number_of_purchases):
        self.Purchaser = webscraper
        self.config = usr_config
        self.num_purchases = number_of_purchases

    def email_purchases_creator(self):
        purchases = ""
        if self.Purchaser.ERR == 0:
            for j in range(0, self.num_purchases):
                purchase = "{SEC} for ${SEC_INV} @{TIME}\n".format(SEC=self.config["security_purchases"][j], SEC_INV=self.config["security_prices"][j], TIME=self.Purchaser.time_purchased[j])
                purchases += purchase
            purchases += "\nTotal Amount Purchased = ${MONEY_TRADED}".format(MONEY_TRADED=sum(list(map(float, self.config["security_prices"][0:self.num_purchases]))))
        else:
            for j in range(0, self.num_purchases):
                purchase = "{SEC} for ${SEC_INV}\n".format(SEC=self.config["security_purchases"][j], SEC_INV=self.config["security_prices"][j])
                purchases += purchase
            purchases += "\nTotal Amount Purchased = ${MONEY_TRADED}".format(MONEY_TRADED=sum(list(map(float, self.config["security_prices"][0:self.num_purchases]))))
        return purchases

    def email_error_msg_creator(self):
        if self.Purchaser.ERR == 1:
            error_msg_body = """\n
                                THERE WAS AN ERROR RUNNING THE PROGRAM
                                Error Message: {ERR}\n""".format(ERR=self.Purchaser.error_msg)
        else:
            error_msg_body = """\nTHERE WAS NO ERROR"""
        return error_msg_body

    def email(self, purchase_summary):
        email_sender = self.config["BotEmail_Username"]  # Bot email
        email_key = self.config["BotEmail_Key"]  # Google App Password
        email_receiver = self.config["User_Email"]  # Real Email that will be checked
        subject = 'Bot Purchase Report'  # Email Subject

        # Email Body (EDIT IF NEEDED)
        body = """Starting Cash Balance = {INIT_ACC_BAL}\nCash Balance Left = ${ACC_BAL}\n\nPurchases:\n{PURCHASES}\n""".format(INIT_ACC_BAL=self.Purchaser.account_balance, ACC_BAL=self.Purchaser.working_balance, PURCHASES=purchase_summary)

        # Formatting Email
        mail = EmailMessage()
        mail['From'] = email_sender
        mail['To'] = email_receiver
        mail['Subject'] = subject
        mail.set_content(body)

        # Logging in and Sending Email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smpt:
            smpt.login(email_sender, email_key)
            smpt.sendmail(email_sender, email_receiver, mail.as_string())
