import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class celtraHomework(unittest.TestCase):
    def setUp(self):
        '''Web driver setup'''
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.driver.maximize_window()

    def test_chrome_open(self):
        '''Just a quick test to see if the browser starts running'''
        driver = self.driver
        driver.get("http://test.celtra.com/preview/f576e12f#overrides.deviceInfo.deviceType=Phone")
        self.driver.implicitly_wait(10)
        self.assertIn("Ad Preview", driver.title)

    def test_do_celtra_homework(self):
        '''The main program where the homework is done'''

        #open chrome browser
        driver = self.driver
        driver.get("http://test.celtra.com/preview/f576e12f#overrides.deviceInfo.deviceType=Phone")
        self.driver.implicitly_wait(10)

        #switch to iframe where expendable is located
        wait = WebDriverWait(driver, 10)
        frame = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
        "#preview-content > div.orientation-enabled.portrait > div.device-container > div > div:nth-child(3) > span > iframe")))
        driver.switch_to.frame(frame)
        driver.switch_to.frame(1)

        #verify presence of expendable banner
        content = driver.find_element(By.ID, "celtra-object-104")
        self.assertTrue(content)
        content.click()

        time.sleep(1)

        #switch to outer iframe
        driver.switch_to.default_content()
        frame = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
        "#preview-content > div.orientation-enabled.portrait > div.device-container > div > div:nth-child(3) > span > iframe")))
        driver.switch_to.frame(frame)

        time.sleep(1)

        #switch to iframe of modal window
        frame = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
        "body > div.notranslate.celtra-expanded-ad > iframe")))
        driver.switch_to.frame(frame)

        #verify content is correctly displayed by searching for element with proper text
        content = driver.find_element(By.XPATH, "//*[contains(text(), 'Modal Unit')]")
        self.assertTrue(content)

        #press modal and verify logo is gone
        content = driver.find_element(By.CSS_SELECTOR, "#celtra-object-41 > div")
        self.assertTrue(content)
        content.click()
        self.assertTrue(wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR,
        "#celtra-object-41 > div"))))

        time.sleep(1)

        #exit modal view
        content = driver.find_element(By.CSS_SELECTOR,
        "#celtra-modal > img.celtra-close-button.touchable.celtra-close-button-up")
        self.assertTrue(content)
        content.click()

        time.sleep(1)

        #switch back to main window and into iframe of expendable banner
        driver.switch_to.default_content()
        frame = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
        "#preview-content > div.orientation-enabled.portrait > div.device-container > div > div:nth-child(3) > span > iframe")))
        driver.switch_to.frame(frame)
        driver.switch_to.frame(1)

        #verify expendable banner is still there
        content = driver.find_element(By.ID, "celtra-object-104")
        self.assertTrue(content)

    def shutDown(self):
        '''Shuts down the browser app'''
        self.driver.close()

if __name__ == "__main__":
    unittest.main()

'''
BONUS question answers:
A: We can use browser vendors to run our code - if it passes there then it is 
surely browser independent.
B: To run a test case on multiple browsers we can expand it with the TestNG framework, which
allows us to run a test case simultaneously on multiple browsers.
C: If we want efficient reporting we can use TestNG as mentioned above, which generates
reports in which we can see how many test cases passed, failed and which were skipped.
Another option is to integrate our project with Katalon Testops, which enables us to track our
test cases live and also generates reports where we can see which test cases are efficient and
which ones aren't.
'''