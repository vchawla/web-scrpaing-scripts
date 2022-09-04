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

# Initialize client
firebase_admin.initialize_app(cred)
db = firestore.client()

# Define a method to save in database
def save(collection_id, document_id, data):
    db.collection(collection_id).document(document_id).set(data)

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
# Find table named "Blockchains by NFT Sales Volume (24 hours)"
table = soup.findAll('table', {'class' : 'js-top-by-sales-table-24h'})[2]

# Loop over all the table rows
table_rows = table.find_all("tr")[1:]
for row in table_rows:
    # Get chain name from a specific DOM element
    chain_name = row.find('span', {'class' : 'summary-sales-table__column-product-name'}).text    
    # print(chain_name)

    # Get sales from a specific DOM element
    sales = row.find_all('td')[2].text.strip()
    sales = float(sales.replace("$", "").replace(",", ""))
    # print(sales)

    # Get previous sales from a specific DOM element
    prev_sales = row.find_all('td')[3].find('span', {'class' : 'js-tooltip'}).attrs["data-original-title"]
    prev_sales = float(prev_sales.replace("$", "").replace(",", ""))
    # print(prev_sales)

    # Get buyers from a specific DOM element
    buyers = row.find_all('td')[4].text.strip()
    buyers = float(buyers.replace("$", "").replace(",", ""))
    # print(buyers)

    # Get transactions from a specific DOM element
    txns = row.find_all('td')[5].text.strip()
    txns = float(txns.replace("$", "").replace(",", ""))    
    # print(txns)

    # Create a JSON data object for saving individual chain data in Firestore
    data = {
        "chainName": chain_name,
        "sales": sales,
        "prevSales": prev_sales,
        "buyers": buyers,
        "txns": txns
    }

    # Call the save method
    save(
    collection_id = "CSBlockchainsBySalesVolume",
    document_id = chain_name,
    data=data
    )

# Close the driver
driver.close()