# SYSTEM IMPORTS
from selenium import webdriver                          # bot framework for chrome
from selenium.webdriver.chrome.options import Options
from tabulate import tabulate                           # print tables pretty
from tqdm import tqdm                                   # progres bar
from typing import List, Tuple                          # I like to type annotate when I know types
import chromedriver_binary                              # needed for selenium
import numpy as np                                      # random choice
import time                                             # debugging


# PYTHON PROJECT IMPORTS


"""
    INSTRUCTIONS:
        please install the packages:
            - selenium
            - chromedriver-binary
            - tqdm
            - tabulate

    if you want to run this code as is! All of these packages are available via pip
"""


ESSENTIALLY_URL: str = "http://www.essentially.net/rsp/play.jsp"


def get_buttons(driver):
    button_root = "/html/body/form/table/tbody/tr/td/"
    rock = driver.find_element_by_xpath(button_root + "input[@alt='Rock']")
    paper = driver.find_element_by_xpath(button_root + "input[@alt='Paper']")
    scissors = driver.find_element_by_xpath(button_root + "input[@alt='Scissor']")

    return [rock, paper, scissors]


def get_your_move(driver):
    your_move_root = "/html/body/table/tbody/tr/td[2]/font/b"
    return driver.find_element_by_xpath(your_move_root).text

def get_opponent_move(driver):
    opponent_move_root = "/html/body/table/tbody/tr/td[3]/font/b"
    return driver.find_element_by_xpath(opponent_move_root).text


def get_result(driver):
    result_root = "/html/body/h3/"
    return driver.find_element_by_xpath(result_root + "blockquote").text


def essentially_scraper(strategy: np.ndarray = None, num_trials: int = 100, headless: bool = False) -> List[List[str]]:

    if strategy is None:
        strategy = np.array([1,1,1]) / 3

    options = Options()
    options.headless = headless

    driver = webdriver.Chrome(options=options)
    driver.get(ESSENTIALLY_URL)

    data: List[List[str]] = list()

    for i in tqdm(range(num_trials), desc="playing rock paper scissors..."):
        button = get_buttons(driver)[np.random.choice(3, p=strategy)]
        button.click()
        data.append([get_your_move(driver), get_opponent_move(driver), get_result(driver)])

    return data

def get_performance_stats(data: List[List[str]]) -> List[int]:
    # format is [num_wins, num_losses, num_ties]
    stats: List[int] = [0,0,0]

    for trial in data:
        result: str = trial[-1]
        if "won" in result.lower():
            stats[0] += 1
        elif "lost" in result.lower():
            stats[1] += 1
        elif "tied" in result.lower():
            stats[2] += 1
        else:
            raise ValueError("ERROR: unknown result: %s" % result)

    return stats

if __name__ == "__main__":
    NUM_TRIALS = 100

    data = essentially_scraper(num_trials=NUM_TRIALS, headless=True)
    print(tabulate(data, headers=["you", "computer", "result"]))

    stats = get_performance_stats(data)
    assert(np.sum(stats) == NUM_TRIALS)
    print(tabulate([stats], headers=["num wins", "num losses", "num ties"]))

