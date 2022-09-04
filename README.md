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

## Projects.py

The file called Projects.py pulls data from a given NFT project from both the websites.<br/>
Data is extracted in same fashion as above scripts. <br/>
The script can be configured to pass a specific project name and Immutable address to fetch its data.<br/>
Extracted data is stored in Firestore.<br/>
The Firestore credentials certificate JSON file should be stored under creds folder in the parent directory (which has been excluded here for security reasons).

## Future enhancements

1.] Currently both these files are to be run manually. But a possible enhancement is to set them as cron jobs so as to run them scheduled interval of time.


## Disclaimer

These crawlers have been implemented for assignment/education purposes. Legal teams of respective websites should be consulted with for any production implementation

### References

[https://oxylabs.io/blog/beautiful-soup-parsing-tutorial](https://oxylabs.io/blog/beautiful-soup-parsing-tutorial) <br/>
[https://www.youtube.com/watch?v=_P0lxYVgjiY](https://www.youtube.com/watch?v=_P0lxYVgjiY) <br/>
[https://www.linkedin.com/pulse/chart-automation-extracting-data-from-html-canvas-element-adhikary/](https://www.linkedin.com/pulse/chart-automation-extracting-data-from-html-canvas-element-adhikary/) <br/>
[https://www.youtube.com/watch?v=i9N_LrnDUnY](https://www.youtube.com/watch?v=i9N_LrnDUnY) <br/>