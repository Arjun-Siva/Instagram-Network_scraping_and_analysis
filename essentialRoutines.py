import time
from collections import Counter
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def dict_to_adjList(allNodes):
    adjList = []
    for person,following in allNodes.items():
        f = " ".join(following)
        adjList.append(person +" "+ f + "\n")
        
    return adjList

def adjList_to_dict(adjList):
    allNodes = {}
    for line in adjList:
        list_of_persons = line.strip('\n').split(" ")
        person = list_of_persons[0]
        following = list_of_persons[1:]
        allNodes[person] = following
        
    return allNodes


def check_if_stuck(prev_scrape_sizes, new_scrape_size):
    occurences = Counter(prev_scrape_sizes)
    for v in occurences.values():
        if v > 38:
            return (True,prev_scrape_sizes)
        
    if len(prev_scrape_sizes) >= 40:
        del prev_scrape_sizes[0]
    prev_scrape_sizes.append(new_scrape_size)
        
    return (False, prev_scrape_sizes)


def login_insta(driver,username,password):
    driver.get("https://www.instagram.com/accounts/login")
    time.sleep(3)
    #driver.save_screenshot('scrnsh.png')
    driver.find_element_by_xpath(
        "//input[@name='username']").send_keys(username)
    driver.find_element_by_xpath(
        "//input[@name='password']").send_keys(password)

    driver.find_element_by_xpath("//button/div[text()='Log In']").click()
    print("Logged in")

        
def get_following_links(driver):
    followList = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.wo9IH span a")))
    links = [name.get_attribute("href") for name in followList]
    return links


def scrape_whole_list(list_to_scrape, driver, link):
    driver.get(link)
    driver.implicitly_wait(3)
    length_of_list = int("".join((driver.find_element_by_xpath("//a[text()=' {}']/span[@class='g47SY ']".format(list_to_scrape)).text).split(",")))

    # wait_time = length_of_list/ 3.5

    driver.find_element_by_xpath("//a[text() = ' {}']".format(list_to_scrape)).click()
    driver.implicitly_wait(2)
    FList = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role=\'dialog\'] ul'))
    )
    numberInList = len(FList.find_elements_by_css_selector('li'))
    scrape_sizes = []
    frame = driver.find_element_by_xpath("//div[@class='isgrP']")
    frame2 = driver.find_element_by_xpath("//div[@class='PZuss']")
    driver.implicitly_wait(0.25)
    if length_of_list > 10:
        size_of_list = frame.size
        w = size_of_list['width']
        ActionChains(driver).move_to_element(frame).perform()
        ActionChains(driver).move_by_offset(0.25*(w),0).click().perform()
        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        driver.implicitly_wait(0.25)
        ActionChains(driver).move_to_element(frame).perform()
        ActionChains(driver).move_by_offset(0.25*(w),0).click().perform()

        # tic = time.perf_counter()

        ActionChains(driver).move_to_element(frame2).perform()
        ActionChains(driver).move_by_offset(0.25*(w),0).click().perform()
    while (numberInList < length_of_list):
        driver.implicitly_wait(0.25) # Tune this according to your internet speed

        ActionChains(driver).move_to_element(frame2).perform()
        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        numberInList = len(FList.find_elements_by_css_selector('li'))

        # Use the below timer function below if you prefer it over "check_if_stuck" method
        # toc = time.perf_counter()
        # if (toc - tic) > wait_time:
        #     if numberInList >= (length_of_list - 5):
        #         break
        #     else:
        #         print("Number in list: {}".format(numberInList))
        #         print("Restarting {}".format(list_to_scrape))
        #         return scrape_whole_list(list_to_scrape, driver, link)

        stop,scrape_sizes = check_if_stuck(scrape_sizes, numberInList)
        if stop:
            if numberInList >= (length_of_list - 5):
                break
            else:
                print("Number in list: {}".format(numberInList))
                print("Restarting {}".format(list_to_scrape))
                return scrape_whole_list(list_to_scrape, driver, link)

    print("scrolling {} done".format(list_to_scrape))
    
    followList = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.wo9IH span a")))
    follow = [name.get_attribute("text") for name in followList]
    return follow