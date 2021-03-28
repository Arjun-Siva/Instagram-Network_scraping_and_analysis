# Instagram-Network_scraping_and_analysis
Python script to scrape "Followers" and "Following" lists of an Instagram account and **also the lists of all accounts in that "Following" list**.

The script can be used to scrape the accounts in small batches. An adjacency list of the connections is created which is directly compatible with Networkx library. The **adjList.txt** file contains nodes represented the form of -

 ``` 
 Node1 Node2 Node3 Node4
 Node2 Node1 Node5
 ```
 where Node1 follows Node2, Node3 and Node4. Similary Node2 follows Node1 and Node 5. Refer [Networkx representation](https://networkx.org/documentation/stable/reference/readwrite/edgelist.html "Networkx representation")
 

## Requirements
1. Python 3.x
2. Mozilla Firefox browser [Download](https://www.mozilla.org/en-US/firefox/new/ "Download")
3. Geckodriver [Download](https://github.com/mozilla/geckodriver/releases "Download")
4. Libraries
    1. Selenium webdriver
    2. Networkx

## Directions for usage
1. Run the **scrapeMyAccount.py** file first to scrape the list of followers and following of your account
2. Once the **followingLinks.txt** is generated, run the **scrapingFollowing.py** file to scrape the "Following" and "Followers" list of the accounts you follow

## Note
1. Run the cells in in correct order. Run the *Scraping in batches* cell in scrapingFollowing.py only after the logging in is successful
2. Scrape in small batches
3. Instagram will temporarily disable your account if you log-in frequently. Check if the account is not disabled before scraping
4. Disable **headless** mode in scrapingFollowing.py if something went wrong to troubleshoot

## Example network graph
![graoh1_yifan_communities](https://user-images.githubusercontent.com/59311154/112763128-c72e8500-9020-11eb-80c9-699e8d397933.png)
The above directed graph portraying my Instagram network consisting of some 80,000 nodes in Yifan Hu layout was generated in Gephi. The nodes in this graph include the "Followers" and "Following" of all the accounts I follow (except accounts with more than 2000 followers). Communities present in the graph are marked by different colors.

![Graph2_Atlas](https://user-images.githubusercontent.com/59311154/112763496-4a9ca600-9022-11eb-9493-61e9e77674b0.png)
The above directed graph is a subset of the previous graph consisting only the accounts I follow and the accounts which follow me. There are noticeable demarcations among my highschool friends circle, middle school friends circle, college friends circle and meme pages. The graph is in ForceAtlas2 layout and was generated in Gephi.

The **Instagram-Network-Analysis.ipynb** contains analysis of my network graph with a few "Off-the-Shelf" functions in Networkx library.
