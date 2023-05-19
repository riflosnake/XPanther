from time import sleep

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from xpanther import XPanther


class XPantherIDE:
    def __init__(self, page_url):
        self.__driver = webdriver.Chrome()
        self.__page_url = page_url

    def wait_for_alert(self):
        for _ in range(100):
            try:
                WebDriverWait(self.__driver, 1).until(ec.alert_is_present())
                sleep(1)
            except TimeoutException:
                return True

    def start(self):
        program_return = []
        self.__driver.get(self.__page_url)
        print("---XPantherIDE Started---")
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
        sweetalert_js = """
                var script = document.createElement('script');
                script.src = 'https://cdn.jsdelivr.net/npm/sweetalert2@10.15.5/dist/sweetalert2.all.min.js';
                document.head.appendChild(script);
                """
        self.__driver.set_script_timeout(10000)
        self.__driver.execute_script(event_js)
        self.__driver.execute_script(sweetalert_js)
        current_url = self.__driver.current_url
        try:
            index = 0
            for _ in range(1000):
                try:
                    if (new_url := self.__driver.current_url) != current_url:
                        current_url = new_url
                        self.__driver.execute_script(event_js)
                        self.__driver.execute_script(sweetalert_js)
                    return_value = WebDriverWait(self.__driver, 1).until(
                        lambda driver: self.__driver.execute_script(return_js)
                    )
                    if return_value:
                        try:
                            self.__driver.execute_script(
                                """
                                    Swal.fire({
                                      position: 'top-end',
                                      text: 'Capturing...',
                                      })"""
                            )
                            xpath = XPanther(
                                return_value[1], print_output=False, speed='fast'
                            ).capture(return_value[0])[0]
                            self.__driver.execute_script(
                                f"""
                                   Swal.fire({{
                                      position: 'top-end',
                                      text: '{xpath}',
                                      timer: 10000,
                                      }})"""
                            )
                        except WebDriverException:
                            self.__driver.execute_script("alert('Capturing...')")
                            xpath = XPanther(
                                return_value[1], print_output=False, speed='fast'
                            ).capture(return_value[0])[0]
                            self.__driver.switch_to.alert.accept()
                            self.__driver.execute_script(f"alert('{xpath}')")
                        index += 1
                        print(f"#{index} SELECTION -> {xpath}")
                        program_return += [xpath]
                        self.wait_for_alert()
                except TimeoutException:
                    pass
        except WebDriverException:
            print("---XPantherIDE Closed---")
            pass
        finally:
            if program_return:
                return program_return
            else:
                print("No Click Was Registered!")
                return False
