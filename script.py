# Step 1: import webdriver - webdrivers
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, ElementNotInteractableException
import pandas as pd
import os
import json

#initialize webdriver. The webdriver is like a robot that helps us interact with the website
driver = webdriver.Chrome()

#get the website link
link = "https://www.flashscore.com"

driver.get(link)

time.sleep(3)

#here, some basic familiarity with browser inspector tools will be useful. We have to identify the element we're looking for by using its locators or selectors (like class name, ID, XPath, etc.)

element_xpath_selector = "/html/body/div[4]/div[1]/div/div[1]/aside/div/div[2]/div[2]/div[1]/div[1]"

#selenium's webdriver has a function which is used to find elements on a web page. The function takes two parameters and can work with different types of html selectors including classnames, 
# css selector, link text, name, partial link text, tag name , id or xpath
#each selector has its own specific use case depending on what were dealing with. For very specific items, the xpath or id selectors are preferred. But for less specific items/elements, we can
# use other selectors. The use case specifies which selector we should use

#in this first example, we are going to locate a specific element by its xpath. And to click the element after its been found is pretty straightforward, we just add the click() function as a suffix  
driver.find_element(by=By.XPATH, value="/html/body/div[4]/div[1]/div/div[1]/aside/div/div[2]/div[2]/div[1]/div[1]").click()

time.sleep(3)

#at this point, lets add a futher functionality to our script to click on another element which we locate using its id
driver.find_element(by=By.ID, value="li5").click()

time.sleep(3)

#now let us add further python logic to help us do something more meaningful. at the current state, our web app is able to click on the archive link so let us try to access all the different leagues
# in a different tab

#notice here we are trying to find multiple elements, so we need to use the find_elements() function which is used to find multiple elements on a webpage. Notice that if we want to find a single
# element, we use find_element(). And if we want to find multiple elements, we use find_elements()
seasons = driver.find_elements(by=By.CLASS_NAME, value='archive__season')

#now we can use a python loop to iterate through each seperate season element and click them.
for season in seasons[1:10]:
    
    #get the link of the season element. notice how we can find an element inside of another element by calling the find_elements() method on the specific element
    season_link = season.find_element(by=By.CLASS_NAME, value="archive__text--clickable")
    season_url = season_link.get_attribute('href')

    # Create a new window/tab
    driver.execute_script("window.open('');")

    # Switch to the new window/tab (it will be the last one opened)
    driver.switch_to.window(driver.window_handles[-1])

    # Navigate to the season URL in the new tab
    driver.get(season_url) 

    time.sleep(4)

    #Here, after navigating to the season's page. We access the season results by finding the xpath then clicking on it
    driver.find_element(by=By.XPATH, value='//*[@id="li2"]').click()

    time.sleep(5)

    #Here, lets show how we'd deal with dynamic content loading and waiting strategies
    while True:
        try:
            # WebDriverWait(driver, timeout).until(
            #     EC.presence_of_element_located((By.CLASS_NAME, "event__more.event__more--static"))
            # )
            button_element = WebDriverWait(driver, 2).until(
                                EC.element_to_be_clickable((By.CLASS_NAME, "event__more.event__more--static"))
                            )
                            
            # Scroll the button into view
            driver.execute_script("arguments[0].scrollIntoView();", button_element)
            
            # Click the button using JavaScript
            driver.execute_script("arguments[0].click();", button_element)

            time.sleep(5)

        except TimeoutException:
            break
    
    #Here, we have loaded all games that happened in a season, so now we want to learn how to deal with popup windows 
    #When we click on each individual match link, a popup window is automaticallhy created and we can switch to that popup window
    all_match_links = driver.find_elements(by=By.CLASS_NAME, value='eventRowLink')
    for match_link in all_match_links:
        
        # Scroll the match link into view
        driver.execute_script("arguments[0].scrollIntoView(true);", match_link)

        # Get the current window handle before clicking
        original_window = driver.current_window_handle

        # Click the link using JavaScript (opens the popup)
        driver.execute_script("arguments[0].click();", match_link)

        # Wait for the new window (popup) to open
        try: 
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(3))

            # Switch to the new window (popup)
            driver.switch_to.window(driver.window_handles[-1])

            # Now you are controlling the popup window
            # Wait for the body element to load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # Print the popup title or scrape the data you need
            print(f"Popup title: {driver.title}")

            # Example: Lets print out the home and away teams, as well as the game results:

            text_content = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[4]').text

            print(f"This is the score and summary: {text_content}")


            # Close the popup window
            driver.close()

            # Switch back to the original window
            driver.switch_to.window(original_window)

            # Wait a bit before clicking the next match link
            time.sleep(2)


        except Exception as e:
                            print(f'Error getting match popup: {str(e)}')
    
    time.sleep(5)

    # Close current tab
    driver.close()

    # Switch back to original tab
    driver.switch_to.window(driver.window_handles[0])