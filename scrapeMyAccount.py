#%% Loading libraries
import time
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
PATH = r"C:\Users\username\Downloads\geckodriver" # Geckodriver path
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
driver = webdriver.Firefox(executable_path=PATH, firefox_options = options)

essentialRoutines.login_insta(driver,username,password)
time.sleep(5)
#%% Scraping my Followers and Following

try:
    not_now_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[text()= 'Not Now']")))
    not_now_button.click()
    
except:
    pass

element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "span._2dbep.qNELH"))
)
element.click()

driver.implicitly_wait(2)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.XPATH, "//div[text()='Profile']"))).click()
driver.implicitly_wait(5)

myFollowers = int("".join((driver.find_element_by_xpath("//a[text()=' followers']/span[@class='g47SY ']").text).split(",")))
myFollowing = int("".join((driver.find_element_by_xpath("//a[text()=' following']/span[@class='g47SY ']").text).split(",")))

driver.find_element_by_xpath("//a[text() = ' followers']").click()
driver.implicitly_wait(3)

allNodes = {}

myUsername = str(driver.find_element_by_tag_name("h2").text)
print(myUsername)
print("Followers: "+str(myFollowers)+", Following: "+str(myFollowing))
my_followers = essentialRoutines.scrape_whole_list("followers", driver, "https://www.instagram.com/"+myUsername)
for follower in my_followers:
    allNodes[follower]=[]
    allNodes[follower].append(myUsername)
    
my_following = essentialRoutines.scrape_whole_list("following", driver, "https://www.instagram.com/"+myUsername)

allNodes[myUsername]=my_following
following_links = essentialRoutines.get_following_links(driver)
driver.close()

#%% Writing into files
list_of_links_with_delimiter = map(( lambda x: x + '\n'), following_links)
with open("followingLinks.txt","w") as file_h:
    file_h.writelines(list_of_links_with_delimiter)


adjList = essentialRoutines.dict_to_adjList(allNodes)

with open("adjList.txt","w") as adj_file:
    adj_file.writelines(adjList)
