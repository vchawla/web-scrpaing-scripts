# Scraping scripts

## cryptoslam.py

The file called cryptoslam.py pulls data from cryptoslam.io website.<br/>
It pulls HTML table called **Blockchains by NFT Sales Volume (24 hours)** from the homepage.<br/>
Extracted data is stored in Firestore.<br/> 
The Firestore credentials certificate JSON file should be stored under creds folder in the parent directory (which has been excluded here for security reasons).


## immutascan_post.py

The file called immutascan_post.py pulls data from immutasca.io website.<br/>
It pulls **Trade Volume chart** from the homepage by invoking the HTTP request which have been obtained using Chrome developer tools.<br/>
Extracted data is stored in Firestore.<br/>
The Firestore credentials certificate JSON file should be stored under creds folder in the parent directory (which has been excluded here for security reasons).

## Future enhancements

1.] Currently both these files are to be run manually. But a possible enhancement is to set them as cron jobs so as to run them scheduled interval of time.
