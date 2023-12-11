from time import sleep, time

from selenium.common.exceptions import TimeoutException, WebDriverException, NoAlertPresentException, InvalidArgumentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from xpanther import XPanther
from selenium.webdriver.chrome.service import Service as ChromeService
from subprocess import CREATE_NO_WINDOW


class XPantherIDE:
    def __init__(self, page_url, advanced=True, GUI=False, language=None):
        chrome_service = ChromeService('chromedriver')
        chrome_service.creation_flags = CREATE_NO_WINDOW
        self.__driver = webdriver.Chrome()
        self.__page_url = page_url

        self.__advanced = advanced
        self.__gui = GUI
        self.__language = language

        self.lang_diff = {
            'Python': ['find_element', 'By.XPATH, \'{}\''],
            'Ruby': ['find_element', ':xpath, \'{}\''],
            'Java': ['findElement', 'By.xpath(\'{}\')'],
            'JavaScript': ['findElement', 'By.xpath(\'{}\')'],
            'Kotlin': ['findElement', 'By.xpath(\'{}\')'],
            'C#': ['FindElement', 'By.XPath(\'{}\')']
        }

        self.__result = ''

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
            return_value[1], print_output=False, speed='fast', show_all=self.__advanced
        ).capture(return_value[0])
        index = 0
        elapsed_time = 0
        if not xpath_s:
            result = 'Could not find XPATH...'
            self.accept_alert()
        else:
            if not self.__advanced:
                xpath_s = [xpath_s[0]]
            result = 'No XPATH found worked with selenium...'
            self.accept_alert()
            for xpath in xpath_s:
                try:
                    start_time = time()
                    element = WebDriverWait(self.__driver, 0.2).until(ec.presence_of_element_located((By.XPATH, xpath)))
                    elapsed_time = (time() - start_time) * 1000
                except TimeoutException or WebDriverException:
                    index += 1
                else:
                    if element == return_value[2]:
                        result = xpath
                        break
        self.__driver.execute_script(f"alert('{result}')")
        return xpath_s, elapsed_time, index

    def print_or_save(self, text):
        if not self.__gui:
            print(text)
        else:
            self.__result += f"{text}\n"

    def start(self):
        program_return = []
        try:
            self.__driver.get(self.__page_url)
        except InvalidArgumentException:
            return False
        self.print_or_save("\033[95m---XPantherIDE Started---\033[0m")
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
                            line_1 = f"\033[97m\n#{index} CLICK -> \033[0m\033[92mTESTED WORKING XPATH:\033[0m"
                            self.print_or_save(line_1)
                            if time_:
                                line_2 = f'\033[96m                 SPEED =< {time_} ms\033[0m\n---------------- {xpath[nr]}'
                            else:
                                line_2 = f'---------------- None'
                            self.print_or_save(line_2)
                            if len(xpath) > 1 or not time_:
                                line_3 = '\033[91m                NOT TESTED/WORKING:\033[0m'
                                self.print_or_save(line_3)
                            for i in range(len(xpath)):
                                if not i == nr:
                                    extra = f'---------------- {xpath[i]}'
                                    self.print_or_save(extra)
                            self.print_or_save('\n')
                            if time_:
                                xpath_syntax_language = self.lang_diff[self.__language]
                                by_xpath = xpath_syntax_language[1].format(xpath[nr])
                                self.print_or_save('{} : element{} = driver.{}({})'.format(self.__language, index, xpath_syntax_language[0], by_xpath))
                                self.print_or_save('\n')
                            if not self.__gui:
                                program_return += xpath
                            else:
                                program_return += [self.__result]
                                self.__result = ''
                        self.wait_for_alert()
                except TimeoutException:
                    pass
        except WebDriverException:
            self.print_or_save("\033[95m---XPantherIDE Closed---\033[0m")
            if program_return:
                if self.__gui:
                    program_return += [self.__result]
                return program_return
            else:
                self.print_or_save("No Click Was Registered!")
                return False
