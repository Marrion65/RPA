import time
import re
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

class NewsExtractor:
    def __init__(self, search_phrase, category, num_months):
        self.search_phrase = search_phrase
        self.category = category
        self.num_months = num_months
        self.driver = webdriver.Safari()  # Use Safari WebDriver

    def navigate_to_website(self):
        self.driver.get("https://www.reuters.com/")  
        time.sleep(3)  

    def search_news(self):
        search_box = self.driver.find_element_by_xpath("//input[@id='searchfield']")
        search_box.send_keys(self.search_phrase)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)

    def select_category(self):
        if self.category:
            category_button = self.driver.find_element_by_xpath("//button[contains(text(), '{}')]".format(self.category))
            category_button.click()
            time.sleep(3)

    def extract_news_data(self):
        # Assuming the news articles are in a list format
        news_articles = self.driver.find_elements_by_xpath("//div[@class='story-content']")

        data = []
        for article in news_articles:
            title = article.find_element_by_xpath(".//h3[@class='story-title']").text
            date = article.find_element_by_xpath(".//time").get_attribute("datetime")
            description = article.find_element_by_xpath(".//p").text
            # Check if title or description contains any mention of money
            money_mention = bool(re.search(r'\$[\d,]+(\.\d+)?\b|\b\d+\s(?:dollars|USD)\b', title + description))
            data.append({
                'Title': title,
                'Date': date,
                'Description': description,
                'Money Mention': money_mention
            })

        return data

    def store_data_in_excel(self, data):
        df = pd.DataFrame(data)
        df.to_excel('news_data.xlsx', index=False)

    def run(self):
        try:
            self.navigate_to_website()
            self.search_news()
            self.select_category()
            news_data = self.extract_news_data()
            self.store_data_in_excel(news_data)
        finally:
            self.driver.quit()

if __name__ == "__main__":
    search_phrase = input("Enter search phrase: ")
    category = input("Enter news category (leave blank if none): ")
    num_months = int(input("Enter number of months for news (0 for current month, 1 for previous month, etc.): "))

    extractor = NewsExtractor(search_phrase, category, num_months)
    extractor.run()
