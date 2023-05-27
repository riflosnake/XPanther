from time import sleep, time

from selenium.common.exceptions import TimeoutException, WebDriverException, NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from xpanther import XPanther


class XPantherIDE:
    def __init__(self, page_url, advanced=True):
        self.__driver = webdriver.Chrome()
        self.__page_url = page_url

        self.advanced = advanced

    def wait_for_alert(self):
        for _ in range(100):
            try:
                WebDriverWait(self.__driver, 1).until(ec.alert_is_present())
                sleep(1)
            except TimeoutException or NoAlertPresentException:
                return True

    def accept_alert(self):
        try:
            self.__driver.switch_to.alert.accept()
        except NoAlertPresentException:
            return None

    def find_and_alert_xpath(self, return_value):
        self.__driver.execute_script("alert('Capturing...')")
        xpath_s = XPanther(
            return_value[1], print_output=False, speed='fast', show_all=self.advanced
        ).capture(return_value[0])[0]
        index = 0
        elapsed_time = 0
        if not xpath_s:
            result = 'Could not find XPATH...'
            self.accept_alert()
        else:
            if not self.advanced:
                xpath_s = [xpath_s]
            result = 'No XPATH found worked with selenium...'
            self.accept_alert()
            for xpath in xpath_s:
                try:
                    start_time = time()
                    element = WebDriverWait(self.__driver, 0.2).until(ec.presence_of_element_located((By.XPATH, xpath)))
                    elapsed_time = (time() - start_time) * 1000
                except TimeoutException:
                    index += 1
                else:
                    if element == return_value[2]:
                        result = xpath
                        break
        self.__driver.execute_script(f"alert('{result}')")
        return xpath_s, elapsed_time, index

    def start(self):
        program_return = []
        self.__driver.get(self.__page_url)
        print("\033[95m---XPantherIDE Started---\033[0m")
        event_js = """
        var array_events = []

        var registerOuterHtml = (e) => {
            e.preventDefault();
            array_events[0] = e.target.outerHTML
            window.array_events = array_events
            }
        var registerUrl = (e) => {
            e.preventDefault();
            array_events[1] = document.documentElement.outerHTML
            array_events[2] = e.target
            }

        getElementHtml = document.addEventListener("contextmenu", registerOuterHtml, true)
        getDOMHtml = document.addEventListener("contextmenu", registerUrl, true)

        """
        return_js = """
        function get_value() {
            var result = window.array_events;
            window.array_events = [];
            return result;
            }
        return get_value()"""
        self.__driver.set_script_timeout(10000)
        self.__driver.execute_script(event_js)
        current_url = self.__driver.current_url
        try:
            index = 0
            for _ in range(9999):
                try:
                    if (new_url := self.__driver.current_url) != current_url:
                        current_url = new_url
                        self.__driver.execute_script(event_js)
                    return_value = WebDriverWait(self.__driver, 1).until(
                        lambda driver: self.__driver.execute_script(return_js)
                    )
                    if return_value:
                        xpath, time_, nr = self.find_and_alert_xpath(return_value)
                        index += 1
                        if xpath:
                            print(f"\033[97m\n#{index} SELECTION -> \033[0m\033[92mTESTED WORKING XPATH:\033[0m")
                            if time_:
                                print(f'\033[96m                 SPEED =< {time_} ms\033[0m')
                                print(f'----------------{xpath[nr]}')
                            else:
                                print(f'----------------None')
                            if len(xpath) > 1 or not time_:
                                print('\033[91m                NOT TESTED/WORKING:\033[0m')
                            for i in range(len(xpath)):
                                if not i == nr:
                                    print(f'----------------{xpath[i]}')
                            print('')
                            program_return += xpath
                        self.wait_for_alert()
                except TimeoutException:
                    pass
        except WebDriverException:
            print("\033[95m---XPantherIDE Closed---\033[0m")
            if program_return:
                return program_return
            else:
                print("No Click Was Registered!")
                return False
