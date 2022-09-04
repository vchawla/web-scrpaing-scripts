import requests
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Path to Firestore credentials certificate
cred = credentials.Certificate("creds/immutable-web-scraping-firebase-adminsdk-nghn0-37e3157d26.json")

# Config for both projects
im_project_name = "Gods Unchained"
im_project_address = "0xacb3c6a43d15b907e8433077b6d38ae40936fe2c"
cs_project_name = "Gods Unchained Immutable"

# Initialize client
firebase_admin.initialize_app(cred)
db = firestore.client()

# Define a method to save in database
def save(collection_id, document_id, data):
    db.collection(collection_id).document(document_id).set(data)


# Immutascan provides data on a date basis and not on a rolling 24 hour basis
# At any given time, the response shall have dynamic/growing data for current date and static data for previous day and backwards
# Thus in order to get data for last 24 hours, we can either run this script towards the end of the current day (around 11.59pm or may be next day 12.01am) or we can ignore current date's data and consider previous date
# Based on the above consideration, there is a configurable variable called "current_day" in this script that needs to be configured
# Configure "current_day" as 1 if we want to consider today's (growing/dynamic) data as current day or configure it as 2 if we want to consider yesterday's data as current day

current_day = 2

# Prepare the Request Body
url = "https://3vkyshzozjep5ciwsh2fvgdxwy.appsync-api.us-west-2.amazonaws.com/graphql"

payload = "{\r\n    \"operationName\": \"getMetricsAll\",\r\n    \"variables\": {\r\n        \"address\": \"" + im_project_address + "\"\r\n    },\r\n    \"query\": \"query getMetricsAll($address: String!) {\\n  getMetricsAll(address: $address) {\\n    items {\\n      type\\n      trade_volume_usd\\n      trade_volume_eth\\n      floor_price_usd\\n      floor_price_eth\\n      trade_count\\n      owner_count\\n      __typename\\n    }\\n    __typename\\n  }\\n  latestTrades(address: $address) {\\n    items {\\n      transfers {\\n        token {\\n          token_address\\n          quantity\\n          token_id\\n          type\\n          usd_rate\\n          __typename\\n        }\\n        __typename\\n      }\\n      txn_time\\n      txn_id\\n      __typename\\n    }\\n    __typename\\n  }\\n}\"\r\n}"
headers = {
  'authority': '3vkyshzozjep5ciwsh2fvgdxwy.appsync-api.us-west-2.amazonaws.com',
  'accept': 'application/json, text/plain, */*',
  'accept-encoding': 'gzip, deflate, br',
  'accept-language': 'en-US,en;q=0.9',
  'content-length': '686',
  'content-type': 'application/json',
  'origin': 'https://immutascan.io',
  'referer': 'https://immutascan.io/',
  'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'cross-site',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
  'x-api-key': 'da2-ihd6lsinwbdb3e6c6ocfkab2nm'
}

# Make the request
response = requests.request("POST", url, headers=headers, data=payload)

# Convert response to JSON object
json_object  = json.loads(response.text)

# Get Total sales for last 24 hours depending on current_day parameter configured above
im_total_sales_last_day = json_object["data"]["getMetricsAll"]["items"][current_day]["trade_volume_usd"]

# Get Total sales for last 7 days depending on current_day parameter configured above
im_total_sales_last_7day = 0
for x in range(0, 7):
    im_total_sales_last_7day = im_total_sales_last_7day + json_object["data"]["getMetricsAll"]["items"][current_day + x]["trade_volume_usd"]

# Get Total sales for last 30 days depending on current_day parameter configured above
im_total_sales_last_30day = 0
for x in range(0, 30):
    im_total_sales_last_30day = im_total_sales_last_30day + json_object["data"]["getMetricsAll"]["items"][current_day + x]["trade_volume_usd"]

# Get Buyers for last 24 hours depending on current_day parameter configured above
im_total_buyers_last_day = json_object["data"]["getMetricsAll"]["items"][current_day]["owner_count"]

# Get Total Buyers for last 7 days depending on current_day parameter configured above
im_total_buyers_last_7day = 0
for x in range(0, 7):
    im_total_buyers_last_7day = im_total_buyers_last_7day + json_object["data"]["getMetricsAll"]["items"][current_day + x]["owner_count"]

# Get Total sales for last 30 days depending on current_day parameter configured above
im_total_buyers_last_30day = 0
for x in range(0, 30):
    im_total_buyers_last_30day = im_total_buyers_last_30day + json_object["data"]["getMetricsAll"]["items"][current_day + x]["owner_count"]

# Get Transactions for last 24 hours depending on current_day parameter configured above
im_total_transactions_last_day = json_object["data"]["getMetricsAll"]["items"][current_day]["trade_count"]

# Get Total Transactions for last 7 days depending on current_day parameter configured above
im_total_transactions_last_7day = 0
for x in range(0, 7):
    im_total_transactions_last_7day = im_total_transactions_last_7day + json_object["data"]["getMetricsAll"]["items"][current_day + x]["trade_count"]

# Get Total Transactions for last 30 days depending on current_day parameter configured above
im_total_transactions_last_30day = 0
for x in range(0, 30):
    im_total_transactions_last_30day = im_total_transactions_last_30day + json_object["data"]["getMetricsAll"]["items"][current_day + x]["trade_count"]



#url of the page to be scraped
url = "https://cryptoslam.io/"
  
# initiating the webdriver. Parameter includes the path of the webdriver.
driver = webdriver.Chrome(ChromeDriverManager().install())
# driver = webdriver.Chrome('./chromedriver') 
driver.get(url) 
  
# this is just to ensure that the page is loaded
time.sleep(5) 
  
html = driver.page_source
  
# this renders the JS code and stores all
# of the information in static HTML code.
  
# Now, we could simply apply bs4 to html variable
soup = BeautifulSoup(html, "html.parser")

# Varaibles to hold data for Last 24 hours
sales_last_day = 0
buyers_last_day = 0
txns_last_day= 0

# Find table named "NFT Collection Rankings by Sales Volume (24 hours)"
table = soup.findAll('table', {'class' : 'js-top-by-sales-table-24h'})[0]

# Loop over all the table rows
table_rows = table.find_all("tr")[1:]
for row in table_rows:
    # Get Collection name from a specific DOM element
    # print(row.find('span', {'class' : 'summary-sales-table__column-product-name'}))
    collection_name = row.find('span', {'class' : 'summary-sales-table__column-product-name'}).text

    if collection_name == cs_project_name:
        # Get sales from a specific DOM element
        sales_last_day = row.find_all('td')[3].text.strip()
        sales_last_day = float(sales_last_day.replace("$", "").replace(",", ""))
        # print(sales)

        # Get buyers from a specific DOM element
        buyers_last_day = row.find_all('td')[5].text.strip()
        buyers_last_day = float(buyers_last_day.replace("$", "").replace(",", ""))
        # print(buyers)

        # Get transactions from a specific DOM element
        txns_last_day = row.find_all('td')[6].text.strip()
        txns_last_day = float(txns_last_day.replace("$", "").replace(",", ""))    
        # print(txns)

        break

# Varaibles to hold data for Last 7 days
sales_last_7day = 0
buyers_last_7day = 0
txns_last_7day= 0

# Find table named "NFT Collection Rankings by Sales Volume (7 days)"
table = soup.findAll('table', {'class' : 'js-top-by-sales-table-7d'})[0]

# Loop over all the table rows
table_rows = table.find_all("tr")[1:]
for row in table_rows:
    # Get Collection name from a specific DOM element
    # print(row.find('span', {'class' : 'summary-sales-table__column-product-name'}))
    collection_name = row.find('span', {'class' : 'summary-sales-table__column-product-name'}).text

    if collection_name == cs_project_name:
        # Get sales from a specific DOM element
        sales_last_7day = row.find_all('td')[3].text.strip()
        sales_last_7day = float(sales_last_7day.replace("$", "").replace(",", ""))
        # print(sales)

        # Get buyers from a specific DOM element
        buyers_last_7day = row.find_all('td')[5].text.strip()
        buyers_last_7day = float(buyers_last_7day.replace("$", "").replace(",", ""))
        # print(buyers)

        # Get transactions from a specific DOM element
        txns_last_7day = row.find_all('td')[6].text.strip()
        txns_last_7day = float(txns_last_7day.replace("$", "").replace(",", ""))    
        # print(txns)

        break


# Varaibles to hold data for Last 30 days
sales_last_30day = 0
buyers_last_30day = 0
txns_last_30day= 0

# Find table named "NFT Collection Rankings by Sales Volume (30 days)"
table = soup.findAll('table', {'class' : 'js-top-by-sales-table-30d'})[0]

# Loop over all the table rows
table_rows = table.find_all("tr")[1:]
for row in table_rows:
    # Get Collection name from a specific DOM element
    # print(row.find('span', {'class' : 'summary-sales-table__column-product-name'}))
    collection_name = row.find('span', {'class' : 'summary-sales-table__column-product-name'}).text

    if collection_name == cs_project_name:
        # Get sales from a specific DOM element
        sales_last_30day = row.find_all('td')[3].text.strip()
        sales_last_30day = float(sales_last_30day.replace("$", "").replace(",", ""))
        # print(sales)

        # Get buyers from a specific DOM element
        buyers_last_30day = row.find_all('td')[5].text.strip()
        buyers_last_30day = float(buyers_last_30day.replace("$", "").replace(",", ""))
        # print(buyers)

        # Get transactions from a specific DOM element
        txns_last_30day = row.find_all('td')[6].text.strip()
        txns_last_30day = float(txns_last_30day.replace("$", "").replace(",", ""))    
        # print(txns)

        break

# Create a JSON data object for saving in Firestore
data = {
        "im_total_sales_last_day": im_total_sales_last_day,
        "im_total_buyers_last_day":im_total_buyers_last_day,
        "im_total_transactions_last_day":im_total_transactions_last_day,
        "im_total_sales_last_7day": im_total_sales_last_7day,
        "im_total_buyers_last_7day":im_total_buyers_last_7day,
        "im_total_transactions_last_7day":im_total_transactions_last_7day,
        "im_total_sales_last_30day": im_total_sales_last_30day,
        "im_total_buyers_last_30day":im_total_buyers_last_30day,
        "im_total_transactions_last_30day":im_total_transactions_last_30day,                
        "cs_total_sales_last_day":sales_last_day,
        "cs_total_buyers_last_day":buyers_last_day,
        "cs_total_transactions_last_day":txns_last_day,
        "cs_total_sales_last_7day":sales_last_7day,
        "cs_total_buyers_last_7day":buyers_last_7day,
        "cs_total_transactions_last_7day":txns_last_7day,
        "cs_total_sales_last_30day":sales_last_30day,
        "cs_total_buyers_last_30day":buyers_last_30day,
        "cs_total_transactions_last_30day":txns_last_30day        
    }

# Call the save method
save(
    collection_id = "Projects",
    document_id = im_project_name,
    data=data
    )



with open("response.txt", "w") as f:
    f.write(response.text)
