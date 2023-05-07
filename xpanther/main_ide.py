from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from xpanther import XPanther

# TODO # 1: The button which gets clicked, doesn't get value in the script, find a way to persist variables through JavaScript
# TODO # 2: iFrames are not supported
# TODO # 3: This should be done with GUI.


class XPantherIDE:
    def __init__(self, page_url):
        self.__driver = webdriver.Chrome()
        self.__page_url = page_url

    def start(self):
        program_return = []
        self.__driver.get(self.__page_url)
        event_js = '''
        var array_events = []
        
        var registerOuterHtml = (e) => {
            array_events.push(e.target.outerHTML)
            window.array_events = array_events
            }
        var registerUrl = (e) => {
            array_events.push(document.documentElement.outerHTML)
            }
            
        getElementHtml = document.addEventListener("click", registerOuterHtml, true)
        getDOMHtml = document.addEventListener("click", registerUrl, true)
        '''
        return_js = '''
        function get_value() {
            var result = window.array_events;
            window.array_events = [];
            return result;
            }
        return get_value()'''
        self.__driver.set_script_timeout(10000)
        self.__driver.execute_script(event_js)
        current_url = self.__driver.current_url
        try:
            for _ in range(1000):
                try:
                    if (new_url := self.__driver.current_url) != current_url:
                        current_url = new_url
                        self.__driver.execute_script(event_js)
                    return_value = WebDriverWait(self.__driver, 1).until(lambda driver: self.__driver.execute_script(return_js))
                    program_return += [[value, html] for value, html in zip(return_value[::2], return_value[1::2]) if value not in (element[0] for element in program_return)]
                except TimeoutException:
                    pass
        except WebDriverException:
            pass
        finally:
            index = 1
            if program_return:
                for click in program_return:
                    print("\033[91m {}\033[00m".format(f'\n#{index} CLICK SELECTION:'))
                    XPanther(click[1]).capture(click[0])
                    index += 1
                return True
            else:
                print('No click was registered!')
                return False
