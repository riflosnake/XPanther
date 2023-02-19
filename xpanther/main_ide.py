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
        self.__element_list = []
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
        return_js = '''return window.array_events'''
        self.__driver.set_script_timeout(10000)
        self.__driver.execute_script(event_js)
        try:
            for _ in range(1800):
                if array_events := self.__driver.execute_script(return_js):
                    if array_events[-2:] not in program_return:
                        program_return.append(array_events[-2:])
                else:
                    try:
                        WebDriverWait(self.__driver, 0.1).until(
                            lambda driver: self.__driver.current_url != self.__page_url)
                    except TimeoutException:
                        pass
                    else:
                        self.__page_url = self.__driver.current_url
                        self.__driver.execute_script(event_js)
        except WebDriverException:
            pass
        finally:
            index = 1
            if program_return:
                for click in program_return:
                    print("\033[91m {}\033[00m".format(f'\n#{index} CLICK SELECTION:'))
                    XPanther(click[1]).capture(click[0])
                    index += 1
            else:
                print('No click was registered!')
