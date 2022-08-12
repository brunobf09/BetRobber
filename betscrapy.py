from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import pandas as pd

def scrapy(league):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('chromedriver', chrome_options=options)

    link = "https://www.betfair.com/sport/football/"

    driver.get(link)

    while (len(driver.find_elements(By.ID,"onetrust-accept-btn-handler"))) < 1:
        sleep(0.1)

    accept = driver.find_element(By.ID,"onetrust-accept-btn-handler")
    accept.click()

    teams = []
    odds_events = []
    date = []

    for l in league:
        driver.get(link + l)
        while (len(driver.find_elements(By.CLASS_NAME, 'ui-runner-price'))) < 1:
            sleep(0.2)
        for odds in driver.find_elements(By.CLASS_NAME, 'ui-runner-price'):
            odds_events.append(odds.text)
        for team in driver.find_elements(By.CLASS_NAME, 'team-name'):
            teams.append(team.text)
        for d in driver.find_elements(By.CLASS_NAME, 'date'):
            date.append(d.text)

    driver.quit()

    odd = odds_events[2::5]
    home = teams[::2]
    away = teams[1::2]

    betfair = {'Date': date,
               'HomeTeam': home,
               'AwayTeam': away,
               'Odd_Betfair': odd}

    print(betfair)
    betfair_df = pd.DataFrame(betfair)

    return betfair_df
