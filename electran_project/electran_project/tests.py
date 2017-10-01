from django.test import LiveServerTestCase, RequestFactory
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from custom_accounts.models import MyUser


class StudentTestCase(LiveServerTestCase):
    def setUp(self):
        """
        Setting up web driver
        """
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(2)

    def test_student_see_question(self):
        """
        Test that a user can login, then find a question, open the question and submit the empty answer field
        :return:
        """
        home_page = self.browser.get('http://127.0.0.1:8000/account/login/')

        # login elements
        username = self.browser.find_element_by_id("id_login")
        password = self.browser.find_element_by_id("id_password")

        # type username and password in browser
        username.send_keys("marji_sound@yahoo.com")
        password.send_keys("5ordibehesht")

        # checks name of log in button and if it can login
        submit_btn = self.browser.find_element_by_css_selector(".electran-login-btn")
        self.assertEqual('Sign In', submit_btn.text)

        submit_btn.click()

        # check brand name of the site
        brand_name = self.browser.find_element_by_xpath("//div[@class='navbar-brand']/a[2]")
        self.assertEqual('Electran', brand_name.text)

        module_selector = self.browser.find_elements_by_id("semesterModule")

        # Checks if there is a module drop down, if yes it needs to have a length of at least 3
        if module_selector:
            my_select = Select(self.browser.find_element_by_xpath("//select[@id='semesterModule']"))
            my_options = [o.text for o in my_select.options]
            self.assertGreater(len(my_options), 2)

            if 'COMPGC03' in my_options:
                selected = 'COMPGC03'
            else:
                selected = my_options[1]

            # select COMPGC03 or if it doesn't exist select the second item in the list
            self.browser.find_element_by_xpath("//select[@name='semester_module']/option[text()='" + selected + "']").click()
            self.browser.find_element_by_css_selector(".electran-submit-btn").click()

        expand_elem = self.browser.find_element_by_xpath("//button[@id='catCollapseAll']")

        expand_elem.click()
        expand_status = expand_elem.get_attribute('innerHTML')

        if expand_status.startswith('Expand'):
            expand_elem.click()

        my_question_elem = self.browser.find_element_by_xpath("//tr[@class='home-question-item']/td/a")

        my_question = my_question_elem.get_attribute('innerHTML')
        self.assertIsNotNone(my_question)

        # print(my_question_elem)

        # click the question
        my_question_elem.click()
        self.browser.implicitly_wait(5)

        # click the submit button in the question page
        submit_answer = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.NAME, "submit")))

        self.assertIsNotNone(submit_answer)
        submit_answer.click()

        # test if the danger error appears
        danger_alert = self.browser.find_element_by_class_name("alert-danger")
        self.assertIsNotNone(danger_alert)

    def tearDown(self):
        self.browser.quit()



