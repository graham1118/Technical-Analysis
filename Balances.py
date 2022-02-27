import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import email
import requests
import imaplib
from imap_tools import MailBox, A
import cryptocompare
import os 
from binance.client import Client
import urllib.parse,  urllib.request
from urllib.parse import urljoin, urlencode
import json, hashlib, hmac, time
from datetime import datetime
import time
import bankdata as bd
import expenses as exp

price_of_dogecoin = cryptocompare.get_price('DOGE', currency = 'USD')['DOGE']['USD']
price_of_polkadot = cryptocompare.get_price('DOT', currency = 'USD')['DOT']['USD']
price_of_bnb = cryptocompare.get_price('BNB', currency = 'USD')['BNB']['USD']


data = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json').json()
price_of_bitcoin = data['bpi']['USD']['rate_float']

fidelity_payload = ['grahamkenan', 'bonelessg18']
fidelity_url = 'https://oltx.fidelity.com/ftgw/fbc/oftop/portfolio#summary/Z40270286'
usaa_payload = ['graham.kenan', 'Bonelessg18#']
usaa_url = 'https://www.usaa.com/my/logon?akredirect=true'

apiKey = 'dxW1mxoFxwHOqN22su73JF4Am1iKZh0NPgMDAc2Yh6nwMp6PjnwdZltirbCowDMK'
secret = 'HraZXUnzi8elERXkoF0yNWFOT7fe1jYrPb9skqEV9DjLR7MyNwSC0VIwuzU0o8E7'
BASE_URL = 'https://api.binance.us'
client = Client(apiKey, secret)
shib_price = client.get_symbol_ticker(symbol="SHIBUSDT")['price']
def getBalances():
    PATH = '/api/v3/account'
    timestamp = int(time.time())
    headers = {
        'X-MBX-APIKEY': apiKey
    }
    params = {
        'recvWindow': 5000,
        'timestamp': client.get_server_time()['serverTime']
    }
    query_string = urllib.parse.urlencode(params)
    params['signature'] = hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BASE_URL, PATH)
    r = requests.get(url, headers=headers, params=params)
    dataSet = r.json()
    return dataSet['balances'][12]['free']

def spacer(x,n):
	if len(str(x)) == n-4:
		x = str(x) + "        "
	if len(str(x)) == n-3:
		x = str(x) + "       "
	if len(str(x)) == n-2:
		x = str(x) + "      "
	if len(str(x)) == n-1:
		x = str(x) + "     "
	if len(str(x)) == n:
		x = str(x) + "    "
	if len(str(x)) == n+1:
		x = str(x) + "   "
	if len(str(x)) == n+2:
		x = str(x) + '  '
	if len(str(x)) == n+3:
		x = str(x) + ' '
	else:
		x = str(x)
	return x

def rev_spacer(x,n):
	if len(str(x)) == n-4:
		x = "        " + str(x)
	if len(str(x)) == n-3:
		x = "       " + str(x)
	if len(str(x)) == n-2:
		x = "      " + str(x)
	if len(str(x)) == n-1:
		x = "     " + str(x)
	if len(str(x)) == n:
		x = "    " + str(x)
	if len(str(x)) == n+1:
		x = "   " + str(x)
	if len(str(x)) == n+2:
		x = '  ' + str(x)
	if len(str(x)) == n+3:
		x = ' ' + str(x)
	else:
		x = str(x)
	return x

def adjust(string):
	if string[-2] == '.':
		string = string + '0'
	if '.' not in string:
		string = string + '.00'
	return string

def PandL(change):
	if float(change) > 0:
		change = '+'+str(change)
	if float(change) == 0:
		change = ' ' + str(change)
	return change

def update_data():
	output_currents = {}
	output_changes = {}
	output_aux = {}
	chrome_options = Options()
	chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
	chrome_options.add_argument("user-data-dir=C:/Users/graham1118/AppData/Local/Google/Chrome/User Data/Default") 
	driver = webdriver.Chrome(executable_path = 'C:/Users/graham1118/AppData/Local/chromedriver_win32/chromedriver.exe', options=chrome_options)

	#USAA
	driver.get(usaa_url)
	username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "input")))
	username.send_keys(usaa_payload[0])
	username.send_keys(Keys.RETURN)
	password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']")))
	password.send_keys(usaa_payload[1])
	password.send_keys(Keys.RETURN)
	email = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label='Email security code to email starting with G and ending in 8@GMAIL.COM']")))
	email.click()
	time.sleep(7)
	with MailBox('imap.gmail.com').login('graham1118@gmail.com', 'bonelessg18', 'INBOX') as mailbox:
		body = [msg.text for msg in mailbox.fetch(A(subject='USAA'))]
		code = str(body[-1][121:127])
	mail = imaplib.IMAP4_SSL("imap.gmail.com")
	mail.login('graham1118@gmail.com', 'bonelessg18')
	mail.select('Inbox')
	success, data = mail.search(None, 'ALL')
	id_list = data[0].split()
	mail.store(id_list[-1], "+FLAGS", "\\Deleted")
	code_input = driver.find_element_by_css_selector("input[name='inputValue']")
	code_input.send_keys(code)
	code_input.send_keys(Keys.RETURN)
	usaa = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ce3eece60a9caf7a2d8214786d975959dde8f441b233f0db9e9285317841c4bd-text-content"]/div/span[2]'))).text
	
	#Fidelity
	driver.get(fidelity_url)
	username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="userId-input"]')))
	password = driver.find_element_by_id("password")
	button = driver.find_element_by_id("fs-login-button")
	username.send_keys(fidelity_payload[0])
	password.send_keys(fidelity_payload[1])
	button.send_keys(Keys.RETURN)
	tab = driver.find_element_by_id('tab-3')
	tab.click()
	ind_balance = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tabContentBalance"]/div[2]/div/div/div[1]/table/tbody/tr[2]/td[2]/span'))).text
	ind_change = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tabContentBalance"]/div[2]/div/div/div[1]/table/tbody/tr[2]/td[3]/span'))).text
	roth_balance = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tabContentBalance"]/div[2]/div/div/div[1]/table/tbody/tr[3]/td[2]/span'))).text
	roth_change = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tabContentBalance"]/div[2]/div/div/div[1]/table/tbody/tr[3]/td[3]/span'))).text
	roth_balance = '$1.00'
	roth_change = '$0.00' #when Roth is deposited into, remove lines 162/163

	#Investopedia
	driver.get('https://www.investopedia.com/simulator/')
	login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="legacy-sim"]/input[2]'))).click()
	username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
	password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
	username.send_keys('graham1118@gmail.com')
	password.send_keys('bonelessg18')
	password.send_keys(Keys.RETURN)
	paper = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Content"]/div[2]/div[2]/div[1]/table[2]/tbody/tr[1]/td[2]/span'))).text
	driver.quit()

	
	#Bitcoin in BlockFi
	#Doge in Kraken
	#SHIB in Atomic Wallet
	
	#Staking:
	    #50 GUSD in Gemini
	    #Polkadot in Kraken
	#AMM-Arb:
	    #0.35 BNB in BlockFi
		#BNB in Trust Wallet
		#USDC in Trust Wallet
	#Pooling:
	    #0.23 CAKE-BNB LP Tokens
	
	output_currents['Roth IRA'] = float(str(roth_balance).replace(',','').replace('$',''))
	output_currents['Fidelity'] = float(str(ind_balance).replace(',','').replace('$',''))
	output_currents['Options'] = 250
	output_currents['Paper'] = float(str(paper).replace(',','').replace('$',''))
	output_currents['Bitcoin'] = round(0.3679*price_of_bitcoin,2) #in blockfi
	output_currents['Dogecoin'] = round(2940*price_of_dogecoin,2) #in kraken
	output_currents['Shiba'] = round(9436824.4623*float(shib_price),2) #in Atomic wallet
	output_currents['Webull'] = round(0.002708*price_of_bitcoin + 500*price_of_dogecoin+80,2) #in webull
	output_currents['Staking'] = round(sum([7.565*price_of_polkadot, .73, 1227.4]),2) #DOT in Kraken, $2 in rewards, GUSD from work
	output_currents['AMM-Arb'] = round(sum([0.349253*price_of_bnb, 2.79, 100]),2) #BNB and USDC in Metamask, 100 USD in Binance US
	output_currents['Pooling'] = round(price_of_bnb*(35/300),2) #in pancakeswap
	output_currents['USAA'] = float(str(usaa).replace(',','').replace('$','')) + 25
	output_currents['Loans'] = 300 #Dad bought 0.1449
	output_currents['Cash'] = 0

	output_changes['Roth IRA'] = float(str(roth_change).replace(',','').replace('$',''))
	output_changes['Fidelity'] = round(100*(output_currents['Fidelity'] / (output_currents['Fidelity'] - float(str(ind_change).replace(',','').replace('$','')))-1),2)
	output_changes['Options'] = 0
	output_changes['Paper'] = round(100*(float(str(paper).replace(',','').replace('$','')) / 100000 - 1),2)
	output_changes['Bitcoin'] = round((100*(round(0.3*price_of_bitcoin,2)/10400-1)),2)
	output_changes['Dogecoin'] = round(100*(output_currents['Dogecoin'] / 1000 - 1),2)
	output_changes['Shiba'] = round(100*(output_currents['Shiba']/83 - 1),2)
	output_changes['Webull'] = round(100*(output_currents['Webull'] / (354.21+80) - 1),2)
	output_changes['Staking'] = round(100*(output_currents['Staking']/(170+50+1185.03)-1),2)
	output_changes['AMM-Arb'] = round(100*(output_currents['AMM-Arb']/(1.79+2.97+98+100)-1),2)
	output_changes['Pooling'] = round(100*(output_currents['Pooling']/35 - 1),2)
	output_changes['USAA'] = 0.00
	output_changes['Loans'] = 0.00
	output_changes['Cash'] = 0.00

	bd0 = open('bankdata.py', 'w')
	bd0.write('currents = ' + repr(output_currents) + '\n')
	bd0.write('changes = ' + repr(output_changes) + '\n')
	bd0.write('aux = ' + repr(output_aux) + '\n')
	bd0.close()

print('\n        ____PORTFOLIO_BALANCES____\n\n  Would you like to update portfolio data \n  since last time running this program?\n  Updating data takes approximately 60s.\n ')
first_response = input('  Update Data? [y/n] \n     --> ')
if first_response == 'y':
	update_data()

import bankdata as bd
currents = bd.currents
currents1 = bd.currents
changes = bd.changes
aux = bd.aux

total = -currents['Paper']
for i in currents.keys():
	total += currents[i]

percents = {}
percent_nums = {}
for i in currents.keys():
	percent_nums[i] = round(100*currents[i]/total,2)
	percents[i] = spacer(adjust(str(percent_nums[i]))+"%",3)


def change(list_of_investments):
	global total, currents, changes
	type_change = 0
	for investment in list_of_investments:
		type_change += currents[investment]*((changes[investment]/100+1)-1)
	type_change = 100*((total + type_change)/total - 1)
	return type_change	

crypto_change = change(['Bitcoin', 'Dogecoin', 'Shiba', 'Webull', 'Staking', 'AMM-Arb', 'Pooling'])
stocks_change = change(['Roth IRA', 'Fidelity'])
bank_change = change(['USAA', 'Loans', 'Cash'])
options_change = change(['Options'])

stock_totals = {'Makeup':spacer(adjust(str(round(percent_nums['Roth IRA'] + percent_nums['Fidelity'],2))) + "%",3), 'Equity':spacer(adjust(str(round(currents['Roth IRA'] + currents['Fidelity'],2))),4), 'P&L':rev_spacer(adjust(str(PandL(round(stocks_change,2)))) + "%",4)}
crypto_totals = {'Makeup':spacer(adjust(str(round(percent_nums['Bitcoin'] + percent_nums['Dogecoin'] + percent_nums['Shiba'] + percent_nums['Webull'] + percent_nums['Staking'] + percent_nums['AMM-Arb'] + percent_nums['Pooling'],2))) + "%",3), 'Equity':spacer(adjust(str(round(currents['Bitcoin'] + currents['Dogecoin'] + currents['Shiba'] + currents['Webull'] + currents['Staking'] + currents['AMM-Arb'] + currents['Pooling'],2))),4), 'P&L':rev_spacer(adjust(str(PandL(round(crypto_change,2)))) + "%",4)}
banking_totals = {'Makeup':spacer(adjust(str(round(percent_nums['USAA'] + percent_nums['Loans'] + percent_nums['Cash'],2))) + "%",3), 'Equity':spacer(adjust(str(round(currents['USAA'] + currents['Loans'] + currents['Cash'],2))),4), 'P&L':rev_spacer(adjust(str(PandL(round(bank_change,2)))) + "%",4)}
options_totals = {'Makeup':spacer(adjust(str(round(percent_nums['Options'],2))) + "%",3), 'Equity':spacer(adjust(str(round(currents['Options'],2))),4), 'P&L':rev_spacer(adjust(str(PandL(round(options_change,2)))) + "%",4)}


for i in currents.keys():
	currents[i] = spacer(adjust(str(round(currents[i],2))),4)
	changes[i] = rev_spacer(adjust(str(PandL(round(changes[i],2)))) + "%",4)

link = {'Roth IRA':'https://oltx.fidelity.com/ftgw/fbc/oftop/portfolio#summary',
		'Fidelity':'https://oltx.fidelity.com/ftgw/fbc/oftop/portfolio#summary',
		'Paper':'https://www.investopedia.com/auth/realms/investopedia/protocol/openid-connect/auth?scope=email&state=01b132a99d668699a1ba12520d03a5af&response_type=code&approval_prompt=auto&redirect_uri=https%3A%2F%2Fwww.investopedia.com%2Fsimulator%2Fhome.aspx&client_id=inv-simulator-conf',
		'Bitcoin':'https://app.blockfi.com/signin',
		'Webull':'https://www.webull.com/',
		'Staking':'https://accounts.binance.us/en/login?return_to=aHR0cHM6Ly93d3cuYmluYW5jZS51cy9lbi9ob21l',
		'AMM-Arb':'https://docs.hummingbot.io/operation/connect-exchange/',
		'Pooling':'https://trustwallet.com/',
		'USAA':'https://www.usaa.com/my/logon?logoffjump=true',
		'PNC':'https://www.onlinebanking.pnc.com/alservlet/PNCOnlineBankingServletLogin',
		'SECU':'https://www.ncsecu.org/',
		'Loans':'https://www.usaa.com/my/logon?logoffjump=true',
		'Cash':'https://www.usaa.com/my/logon?logoffjump=true'}


print('$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$\n$')
print(f'             Position   Status    Makeup    Equity      P&L           Platforms & Positions (To be updated upon strategy completion)')
print(f"\n                                  {stock_totals['Makeup']}  ${stock_totals['Equity']} {stock_totals['P&L']}")
print(f" Active=======================================================")
print(f"           > Roth IRA | OFFLINE | {percents['Roth IRA']}| ${currents['Roth IRA']}|{changes['Roth IRA']} |           Fidelity -- Awaiting $2000 contribution from Omi + Stefanie")
print(f"           > Options  | FUNDED  | {percents['Options']}| ${currents['Options']}|{changes['Options']} |           Tastytrade, Webull -- $170 , $80")
print(f"           > Scalping | FUNDED  | {percents['Scalping']}| ${currents['Scalping']}|{changes['Scalping']} |           Binance -- Bitcoin Scalping")
print(f"           > AMM-Arb  | FUNDED  | {percents['AMM-Arb']}| ${currents['AMM-Arb']}|{changes['AMM-Arb']} |          Bitsgap -- BTC-USDT")
print(f"\n                                  {crypto_totals['Makeup']}  ${crypto_totals['Equity']} {crypto_totals['P&L']}")
print(f" Passive=======================================================")

print(f"           > ETFs | ONLINE  | {percents['Fidelity']}| ${currents['Fidelity']}|{changes['Fidelity']} |           Fidelity -- 10 shares of ARKX")
print(f"           > HODLing  | ONLINE  | {percents['Bitcoin']}| ${currents['Bitcoin']}|{changes['Bitcoin']} |           0.3679 BTC in BlockFi, Gemini")           
print(f"           > Staking  | ONLINE  | {percents['Staking']}| ${currents['Staking']}|{changes['Staking']} |           7.565 DOT, 625.75 GUSD")
print(f"           > Pooling  | ONLINE  | {percents['Pooling']}| ${currents['Pooling']}|{changes['Pooling']} |           CAKE-BNB on Pancakeswap")

print(f"           > Paper    | ONLINE  |   --   | ${spacer(round(float(currents1['Paper'])),4)}|{changes['Paper']} |           $100,000 starting balance")            
print(f"           > Bitcoin  | ONLINE  | {percents['Bitcoin']}| ${currents['Bitcoin']}|{changes['Bitcoin']} |           0.3679 BTC in BlockFi, Gemini")           
print(f"           > Dogecoin | ONLINE  | {percents['Dogecoin']}| ${currents['Dogecoin']}|{changes['Dogecoin']} |           2940 DOGE")       
print(f"           > Shiba    | ONLINE  | {percents['Shiba']}| ${currents['Shiba']}|{changes['Shiba']} |           9,436,824 SHIB")       
print(f"           > Webull   | ONLINE  | {percents['Webull']}| ${currents['Webull']}|{changes['Webull']} |           500 DOGE, 0.0027 BTC")
print(f"\n                                  {banking_totals['Makeup']}  ${banking_totals['Equity']} {banking_totals['P&L']}")
print(f"Banking=======================================================")
print(f"           > USAA     | ONLINE  | {percents['USAA']}| ${currents['USAA']}|{changes['USAA']} |           Primary Checking")
print(f"           > Loans    | ONLINE  | {percents['Loans']}| ${currents['Loans']}|{changes['Loans']} |           $300 flying cards")
print(f"           > Cash     | ONLINE  | {percents['Cash']}| ${currents['Cash']}|{changes['Cash']} |           Tips from Cafe")
print(f"            **************************************************")
print(f"                                           ${round(total,2)} ")
print('\n--> Staking, Loans, and AMM-Arb must be manually updated')
expenses = sum(exp.amount)
print(f'--> Total Expenses: ${expenses}\n')
view_expenses = input('Would you like to see a breakdown of purchases? [y/n] ')
print('\n')
if view_expenses == 'y':
	pd.set_option('display.max_rows', 20)
	
	exp_df = pd.DataFrame(index = exp.date, columns = ['For','Amount'])
	exp_df['For'] = exp.detail
	exp_df['Amount'] = exp.amount
	print(exp_df)
	print(f'                 Total:   {sum(exp.amount)}')
else:
	pass
print('_______________________________________________________________________________________________________________________')

