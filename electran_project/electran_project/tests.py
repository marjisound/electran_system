from django.test import LiveServerTestCase
from selenium import webdriver


class StudentTestCase(LiveServerTestCase):
    def setUp(self):

        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(2)

    def test_student_see_question(self):
        """
        Test that a user can find a question
        :return:
        """
        home_page = self.browser.get('http://127.0.0.1:8000/account/login/')

        # login
        username = self.browser.find_element_by_id("id_login")
        password = self.browser.find_element_by_id("id_password")

        username.send_keys("marji_sound@yahoo.com")
        password.send_keys("")

        # check name of log in button and if it can login
        submit_btn = self.browser.find_element_by_css_selector(".electran-login-btn")
        self.assertEqual('Sign In', submit_btn.text)

        submit_btn.click()

        # check brand name of the site
        brand_name = self.browser.find_element_by_xpath("//div[@class='navbar-brand']/a[2]")
        self.assertEqual('Electran', brand_name.text)

        # Student can find the list of questions that he can pick to answer
        # Hex to Binary Conversion 1
        hex_to_binary_question = self.browser.find_element_by_xpath("//a[@href='/questions/hex_to_binary/']")
        self.assertEqual('Hex to Binary Conversion 1', hex_to_binary_question)

        self.assertIsNotNone(self.browser.find_element_by_xpath("//div[@class='panel-body']/a").text)

        self.fail('Incomplete Test')

    def tearDown(self):
        self.browser.quit()



