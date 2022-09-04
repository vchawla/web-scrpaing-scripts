import requests
import json
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


# Immutascan provides data on a date basis and not on a rolling 24 hour basis
# At any given time, the response shall have dynamic/growing data for current date and static data for previous day and backwards
# Thus in order to get data for last 24 hours, we can either run this script towards the end of the current day (around 11.59pm or may be next day 12.01am) or we can ignore current date's data and consider previous date
# Based on the above consideration, there is a configurable variable called "current_day" in this script that needs to be configured
# Configure "current_day" as 1 if we want to consider today's (growing/dynamic) data as current day or configure it as 2 if we want to consider yesterday's data as current day

current_day = 2

# Prepare the Request Body
url = "https://3vkyshzozjep5ciwsh2fvgdxwy.appsync-api.us-west-2.amazonaws.com/graphql"

payload = "{\r\n    \"operationName\": \"getMetricsAll\",\r\n    \"variables\": {\r\n        \"address\": \"global\"\r\n    },\r\n    \"query\": \"query getMetricsAll($address: String!) {\\n  getMetricsAll(address: $address) {\\n    items {\\n      type\\n      trade_volume_usd\\n      trade_volume_eth\\n      floor_price_usd\\n      floor_price_eth\\n      trade_count\\n      owner_count\\n      __typename\\n    }\\n    __typename\\n  }\\n  latestTrades(address: $address) {\\n    items {\\n      transfers {\\n        token {\\n          token_address\\n          quantity\\n          token_id\\n          type\\n          usd_rate\\n          __typename\\n        }\\n        __typename\\n      }\\n      txn_time\\n      txn_id\\n      __typename\\n    }\\n    __typename\\n  }\\n}\"\r\n}"
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
total_sales_last_day = json_object["data"]["getMetricsAll"]["items"][current_day]["trade_volume_usd"]

# Get Total sales for previous 24 hours depending on current_day parameter configured above
total_sales_prev_day = json_object["data"]["getMetricsAll"]["items"][current_day+ 1]["trade_volume_usd"]

# Get Difference in Total sales between last day and previous day depending on current_day parameter configured above
change_in_sales_today_yesterday = total_sales_last_day - total_sales_prev_day


# print(total_sales_last_day)
# print(total_sales_prev_day)
# print(change_in_sales_today_yesterday)

# Create a JSON data object for saving in Firestore
data = {
        "total_sales_last_day": total_sales_last_day,
        "change_in_sales_today_yesterday": change_in_sales_today_yesterday
    }

# Call the save method
save(
    collection_id = "IMTradeVolume",
    document_id = "Aggregate",
    data=data
    )



# with open("response.txt", "w") as f:
#     f.write(response.text)
