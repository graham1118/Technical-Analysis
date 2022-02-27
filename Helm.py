import subprocess
import os
import expenses as exp
import datetime
import pandas
import time
import math
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def execute_paper_trades(ticker, path):
	if path == '2':
		chrome_options = Options()
		chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
		#chrome_options.add_argument('--headless')
		chrome_options.add_argument("user-data-dir=C:/Users/graham1118/AppData/Local/Google/Chrome/User Data/Default") 

		driver = webdriver.Chrome('C:/Users/graham1118/AppData/Local/chromedriver_win32/chromedriver.exe', options=chrome_options)
		driver.get('https://www.investopedia.com/simulator/')
		login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="legacy-sim"]/input[2]'))).click()
		username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
		password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
		username.send_keys('graham1118@gmail.com')
		password.send_keys('bonelessg18')
		password.send_keys(Keys.RETURN)
		arrow = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Content"]/div[1]/ul/li[4]/span')))
		arrow.click()
		trade = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Content"]/div[1]/ul/li[4]/ul/li[1]/a')))
		trade.click()

		ticker_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "symbolTextbox")))
		ticker_box.send_keys(ticker)
		ticker_box.send_keys(Keys.RETURN)
		price_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Table2"]/tbody/tr[1]/td')))

		quantity = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "quantityTextbox")))
		quantity.send_keys(str(math.floor(2000 / float(price_box.text))))

		preview = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "previewButton")))
		preview.send_keys(Keys.RETURN)

		submit = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "submitOrder")))
		submit.send_keys(Keys.RETURN)
		driver.quit()

		if datetime.datetime.now().hour < 16:
			print('Order Executed')
		else:
			print('Order filed - will execute during next trading day (9:30a-4p EST)')
	elif path == '1':
		fidelity_url = 'https://oltx.fidelity.com/ftgw/fbc/oftrade/EntrOrder?FRAME_LOADED=Y&NAVBAR=Y'
		fidelity_payload = ['grahamkenan', 'bonelessg18']
		chrome_options = Options()
		chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
		#chrome_options.add_argument('--headless')
		chrome_options.add_argument("user-data-dir=C:/Users/graham1118/AppData/Local/Google/Chrome/User Data/Default") 

		driver = webdriver.Chrome('C:/Users/graham1118/AppData/Local/chromedriver_win32/chromedriver.exe', options=chrome_options)
		driver.get(fidelity_url)
		username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="userId-input"]')))
		password = driver.find_element_by_id("password")
		button = driver.find_element_by_id("fs-login-button")
		username.send_keys(fidelity_payload[0])
		password.send_keys(fidelity_payload[1])
		button.send_keys(Keys.RETURN)
		tab = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="form"]/table/tbody/tr[2]/td/input')))
		tab.send_keys(Keys.RETURN)
		symbol = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'eq-ticket-dest-symbol')))
		symbol.send_keys(ticker)
		symbol.send_keys(Keys.RETURN)
		buy = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/app-component/div/order-entry/div[1]/div/div/form/div[1]/div/order-selection/div/div[2]/div[1]/div[1]/div/a[1]/label/span')))
		buy.click()
		shares = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/app-component/div/order-entry/div[1]/div/div/form/div[1]/div/order-selection/div/div[2]/div[1]/div[2]/div/a[1]/label/span')))
		shares.click()
		num_shares = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="eqt-shared-quantity"]')))
		num_shares.send_keys('1')
		market = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/app-component/div/order-entry/div[1]/div/div/form/div[1]/div/order-selection/div/div[2]/div[2]/div/div[1]/a[1]/label/span')))
		market.click()
		preview = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="previewOrderBtn"]')))
		preview.click()

link = {'Roth IRA':'https://oltx.fidelity.com/ftgw/fbc/oftop/portfolio#summary',
		'Fidelity':'https://oltx.fidelity.com/ftgw/fbc/oftop/portfolio#summary',
		'Paper':'https://www.investopedia.com/auth/realms/investopedia/protocol/openid-connect/auth?scope=email&state=01b132a99d668699a1ba12520d03a5af&response_type=code&approval_prompt=auto&redirect_uri=https%3A%2F%2Fwww.investopedia.com%2Fsimulator%2Fhome.aspx&client_id=inv-simulator-conf',
		'Bitcoin':'https://app.blockfi.com/signin',
		'Dogecoin': 'https://www.kraken.com/sign-in',
		'Shiba':'https://www.cointracker.io/wallet/ethereum',
		'Webull':'https://www.webull.com/',
		'Staking':'https://accounts.binance.us/en/login?return_to=aHR0cHM6Ly93d3cuYmluYW5jZS51cy9lbi9ob21l',
		'AMM-Arb':r"C:\Program Files (x86)\Hummingbot\bot.exe",
		'Pooling':'https://pancakeswap.finance/farms',
		'USAA':'https://www.usaa.com/my/logon?logoffjump=true',
		'PNC':'https://www.onlinebanking.pnc.com/alservlet/PNCOnlineBankingServletLogin',
		'SECU':'https://www.ncsecu.org/',
		'Loans':'No link here... Currently you owe Mom and Dad, while Mom owes you $300',
		'Cash':'No link here... check behind piano'}

def prompt():
	global link
	x = input('\nWhat would you like to do?\n     1) View Balances\n     2) View Strategies\n     3) Buy Tickers\n     4) Individual Screener\n     5) Add Expense\n     6) Exit\n     --> ')
	
	if x == '1':
		exec(open('Balances.py').read(), globals())
		exec(open('Helm.py').read(), globals())
		print('_______________________________________________________________________________________________________________________')
		prompt()
	elif x == '2':
		path = input('Here are your strategies:\n     1) Screener\n     2) Crypto Scalping\n     3) Options\n     --> ')
		if path == '1':
			exec(open('Screener.py').read(), globals())
		elif path == '2':
			exec(open('Scalper.py').read(), globals())
		elif path == '3':
			exec(open('Screener.py').read(), globals())
		exec(open('Helm.py').read(), globals())
		print('_______________________________________________________________________________________________________________________')
		prompt()
	elif x == '3':
		pathway = input('Will you be buying real or paper?\n     1) Real\n     2) Paper\n     --> ')
		execute_paper_trades(ticker, pathway)
		
	elif x == '4':
		exec(open('Tester.py').read(), globals())
		exec(open('Helm.py').read(), globals())
		print('_______________________________________________________________________________________________________________________')
		prompt()
	elif x =='5':
		print('Type \'q\' at any point to quit.\n=================================\n')
		x = 1
		while x > 0:
			Amount = input('Expenditure Amount: ')
			if Amount == 'q':
				x = 0
				break
			else:
				Amount = round(float(Amount),2)
			For = input('Brief Description: ')
			if For == 'q':
				x = 0
				break
			Date = f'{datetime.datetime.now().month}/{datetime.datetime.now().day}'
			f = exp.detail
			a = exp.amount
			d = exp.date
			
			f.append(For)
			a.append(Amount)
			d.append(Date)
			bd0 = open('expenses.py', 'w')
			bd0.write('detail = ' + repr(f) + '\n')
			bd0.write('amount = ' + repr(a) + '\n')
			bd0.write('date = ' + repr(d) + '\n')
			bd0.close()
			print('Expense Added\n')
		print('_______________________________________________________________________________________________________________________')
		prompt()
	elif x == '6':
		quit()
	else:
		print('Please enter a number that is in the list')
		prompt()
prompt()