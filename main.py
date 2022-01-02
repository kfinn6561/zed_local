import startup_tools
import bidding
import time
'''
This program loads horse urls and bid amounts from a file called 'bids.csv' and places the appropriate bids on Zed

The following setup is required:
Google chrome must be installed
the metamask extension must be installed
the selenium chromedriver.exe file must be downloaded

The following environment variables must be set
CHROMEDRIVER_PATH 			path of the chromedriver.exe file
METAMASK_EXTENSION_PATH		path of the metamask extension installation
METAMASK_PHRASE    			secret phrase needed to log into metamask
METAMASK_PASSWORD			password for metamask
'''

BIDS_FNAME='bids.csv'

MAX_TRIES=3

print('initialising driver')
driver=startup_tools.initilise_driver()
time.sleep(2)
print('logging in to metamask')
startup_tools.login_metamask(driver)
time.sleep(2)
print('connecting to opensea')
startup_tools.connect_to_opensea(driver)
time.sleep(2)
print('successfully completed startup procedure')
urls,amounts=bidding.get_new_bids(BIDS_FNAME)

print('placing %d bids' %len(urls))

for i in range(len(urls)):
	for j in range(MAX_TRIES):
		if bidding.place_bid(driver,urls[i],amounts[i]):
			break
		else:
			print('Bidding failed (attempt %d of %d)' %(j+1,MAX_TRIES))

driver.quit()