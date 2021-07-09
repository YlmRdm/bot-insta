from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import sys


def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()


class InstagramBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()

    def closeBrowser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        # driver.implicitly_wait(5)
        driver.get("https://www.instagram.com/accounts/login/")
        # time.sleep(10)
        # login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        # login_button = driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]')
        # login_button.click()

        login_link = driver.find_element_by_xpath("//a[text()='Giriş Yap']")
        login_link.click()

        time.sleep(2)
        user_name_elem = driver.find_element_by_xpath(
            "//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)
        passworword_elem = driver.find_element_by_xpath(
            "//input[@name='password']")
        passworword_elem.clear()
        passworword_elem.send_keys(self.password)
        passworword_elem.send_keys(Keys.RETURN)
        time.sleep(2)

    # TODO: Trying to figure it out about action blocked...
    def like_photo(self, hashtag):
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)

        # gathering photos
        pic_hrefs = []
        for i in range(1, 7):
            try:
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                # get tags
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute(
                    'href') for elem in hrefs_in_view if '.com/p/' in elem.get_attribute('href')]
                # building list of unique photos
                [pic_hrefs.append(href)
                 for href in hrefs_in_view if href not in pic_hrefs]
                # print("Check: pic href length " + str(len(pic_hrefs)))
            except Exception:
                continue

        # Liking photos
        unique_photos = len(pic_hrefs)
        for pic_href in pic_hrefs:
            driver.get(pic_href)
            time.sleep(3)
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            try:
                time.sleep(random.randint(2, 4))
                #like_button = lambda: driver.find_element_by_xpath("//span[@aria-label='Beğen']").click()
                # like_button().click()
                driver.find_element_by_class_name("fr66n").click()
                for second in reversed(range(0, random.randint(1, 5))):
                    print_same_line("#" + hashtag + ': unique photos left: ' +
                                    str(unique_photos) + " | Sleeping " + str(second))
                    time.sleep(1)
            except Exception as e:
                time.sleep(3)
            unique_photos -= 1


if __name__ == "__main__":

    username = "USERNAME"
    password = "PASSWORD"

    ig = InstagramBot(username, password)
    ig.login()

    hashtags = ['nature', 'airbnb', 'mountains', 'green', 'likeforlike',
                'Barcelona', 'Russia', 'Georgia', 'Tbilis', 'Baku', ]

    comments = ['Nice pic.', 'Amazing!', 'Great Shot!', 'Looking good!', 'OH MAH GOSH!!',
                'Classic', 'Nice shot!!', 'Ou la la', 'Gorgeous!!', 'cute!', 'Enjoy!!', 'Inspirational',
                'Soooooo cute!!', 'Impressive picture.', 'This picture is lit!!', 'Adorable picture.', 'A good one ✌', 'Amazing post', '#photooftheday',
                'Pretty picture', 'Hi! Observe my profile ASAP!', 'Great!', '😄😄', '⭐', '🐙', 'Fantastic!!',
                'Powerful!', 'Such a cool picture.', 'Best photo ever', 'Irresistible!', 'Elegant picture.', 'Such a charming picture.', 'This picture is better than better']

    while True:
        try:
            # Choose a random tag from the list of tags
            tag = random.choice(hashtags)
            ig.like_photo(tag)
        except Exception:
            ig.closeBrowser()
            time.sleep(60)
            ig = InstagramBot(username, password)
            ig.login()
