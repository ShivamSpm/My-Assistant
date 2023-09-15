from selenium import webdriver


class playVideo():
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path='E:/chromedriver_win32/chromedriver.exe')

    def play(self, query):
        self.query = query
        self.driver.get(url="https://www.youtube.com/results?search_query=" + query)
        firstVideo = self.driver.find_element_by_xpath('//*[@id="dismissible"]')
        firstVideo.click()



