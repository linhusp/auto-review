from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import getpass

account = input("account: ")
password = getpass.getpass("password: ")
score = input("scores: ")


def main():
    my_bot = ReviewBot(account, password)
    my_bot.login()
    my_bot.review(score)
    my_bot.close()


class ReviewBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome()

    def login(self):
        self.browser.get("http://teaching-quality-survey.tdt.edu.vn")
        time.sleep(1)
        username_box = self.browser.find_element_by_xpath(
            '//input[@id="txtUser"]')
        username_box.clear()
        username_box.send_keys(self.username)
        password_box = self.browser.find_element_by_xpath(
            '//input[@id="txtPass"]')
        password_box.clear()
        password_box.send_keys(self.password)
        password_box.send_keys(Keys.RETURN)

    def review(self, score):
        time.sleep(2)
        rfilter = "__doPostBack"
        hrefs = self.browser.find_elements_by_tag_name("a")
        hrefs = [href.get_attribute("href") for href in hrefs]
        review_links = [href for href in hrefs if rfilter in href]

        for i in range(len(review_links)):
            x = "('gvMonHoc','Select$" + str(i) + "')"
            review_link = self.browser.find_element_by_xpath(
                '//a[@href="javascript:__doPostBack' + x + '"]')
            review_link.click()
            review_buttons = self.browser.find_elements_by_xpath(
                '//input[@value="rd' + str(int(score) - 1) + '"]')

            for button in review_buttons:
                button.click()

            try:
                self.browser.find_element_by_xpath(
                    '//input[@id="btnTiepTuc"]').click()
                time.sleep(1)
            except:
                pass

            try:
                self.browser.find_element_by_xpath(
                    '//input[@id="btnTiepTucDanhGia"]').click()
                time.sleep(1)
            except:
                pass

    def close(self):
        self.browser.close()


if __name__ == '__main__':
    main()
