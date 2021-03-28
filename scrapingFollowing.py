#%% Loading libraries
import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
import essentialRoutines
#%% Logging in
username = input("Enter username: ")
password = input("Enter password:")
options = Options()
PATH = r"C:\Users\username\Downloads\geckodriver"  # Geckodriver path
options.add_argument("--headless")  # To run the browser in headless mode
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
driver = webdriver.Firefox(executable_path=PATH, options=options)

essentialRoutines.login_insta(driver,username,password)
time.sleep(5)
#%% Scraping one account
def scrape_data():
    links_file = open("followingLinks.txt","r")
    links = links_file.readlines()
    links_file.close()
    
    adjFile = open("adjList.txt","r")
    adjList = adjFile.readlines()
    adjFile.close()
    allNodes = essentialRoutines.adjList_to_dict(adjList)
    
    driver.get(links[-1])
    try:
        curr_username = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "//div[@class='nZSzR']/h2"))).text
    except:
        curr_username = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "//div[@class='nZSzR']/h1"))).text

    print("Scraping "+curr_username)
    try:
        curr_Followers = int("".join((driver.find_element_by_xpath("//a[text()=' followers']/span[@class='g47SY ']").text).split(",")))
    except:
        print("No follower found")
        curr_Followers = 0
    try:
        curr_Following = int("".join((driver.find_element_by_xpath("//a[text()=' following']/span[@class='g47SY ']").text).split(",")))
    except:
        curr_Following = 0
        print("No following found")
    
    print("{}:Followers:{}, Following:{}".format(curr_username,curr_Followers,curr_Following))
    if curr_Followers < 2000 and curr_Following < 2000:

        # followers
        if curr_Followers > 0:
            followers = essentialRoutines.scrape_whole_list("followers", driver, links[-1])
            print(len(followers))

            for follower in followers:
                try:
                    allNodes[follower].append(curr_username)
                except:
                    allNodes[follower]=[]
                    allNodes[follower].append(curr_username)
        
        # following
        if curr_Following > 0:
            following = essentialRoutines.scrape_whole_list("following", driver, links[-1])
            print(len(following))

            allNodes[curr_username] = following
        
        adjList = essentialRoutines.dict_to_adjList(allNodes)

    del links[-1]
    with open("followingLinks.txt","w+") as file_h:
        file_h.writelines(links)
        
    with open("adjList.txt","w+") as adjFile:
        adjFile.writelines(adjList)

#%% Scraping in batches
for _ in range(5):  # Run this cell only after logging in is successful
    links_file = open("followingLinks.txt","r")
    links = links_file.readlines()
    links_file.close()
    if len(links) != 0:
        try:
            scrape_data()
            print("Successfully scraped 1 profile")
        except:
            traceback.print_exc()
    print("Scraping next after 5 sec")
    time.sleep(5)
#%% Closing the driver
driver.close() # Run this cell only when you are done
