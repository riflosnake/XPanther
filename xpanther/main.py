import re
import requests
from itertools import combinations
from collections import Counter
from bs4 import BeautifulSoup


class XPanther:
    def __init__(self, DOM, xml=False, pre_formatted=False, url_input=False, child_method=True, print_output=True,
                 no_digits=False, show_all=False, speed='normal'):
        self.__dom = DOM
        self.__keys = []
        self.__formatted_html_lines = []
        self.__target = None
        self.__original_target = None
        self.__identical = False
        self.__children_index = []
        self.__gen = []
        self.__child_method = child_method
        self.__child_method_ban = not child_method
        self.__xml = xml
        self.__pre_formatted = pre_formatted
        self.__identifier_method = None
        self.__no_digits = no_digits
        self.__url_input = url_input
        self.__show_all = show_all
        self.__print_output = print_output
        self.__speed = speed

    def capture(self, target):
        program_return = []
        formatted_HTML = self.__format_html(self.__dom)
        element_regex, attr_regex, closing_tag_regex = self.__regex_distributor(formatted_HTML)

        self.__process_html(formatted_HTML, element_regex, attr_regex, closing_tag_regex)

        if type(target) == str and re.match(element_regex, target):
            list_of_occurrences = []
            formatted_element = self.__format_html(target, format_override=True)

            for line in formatted_element:
                if re.match(closing_tag_regex, line.lstrip()):
                    pass
                else:
                    if self.__xml:
                        if not self.__pre_formatted:
                            occurrence = [i for i, x in enumerate(self.__formatted_html_lines) if
                                          Counter(x[:-1]) == Counter(line.lstrip()[:-2])]
                        else:
                            occurrence = [i for i, x in enumerate(self.__formatted_html_lines) if
                                          Counter(x) == Counter(line.lstrip())]
                    else:
                        occurrence = [i for i, x in enumerate(self.__formatted_html_lines) if
                                      Counter(x) == Counter(line.lstrip())]
                    list_of_occurrences.append(occurrence)
            indexes_of_element = []
            if len(list_of_occurrences[0]) > 1:
                if len(formatted_element) > 1:
                    successive_pattern = lambda lists: set(lists[0]).intersection(
                        *({x - i for x in l} for i, l in enumerate(lists[1:], start=1)))
                    successive_pattern = [x for x in successive_pattern(list_of_occurrences)]
                    try:
                        if len(successive_pattern) > 1:
                            self.__print("\033[95m {}\033[00m".format(
                                f'Element is identical to {len(successive_pattern) - 1} other element/s || w/o context highest index \u2B07 is preferred'))
                            self.__identical = True
                        for pattern in successive_pattern:
                            indexes_of_element.append(list_of_occurrences[0].index(pattern))
                    except IndexError:
                        self.__print('Program couldn\'t find this element in DOM, make sure it is inputted correctly !')
                        return False
                else:
                    indexes_of_element = [i for i, x in enumerate(list_of_occurrences[0])]
                    self.__print("\033[95m {}\033[00m".format(
                        f'Element is identical to {len(indexes_of_element) - 1} other element/s || w/o context highest index \u2B07 is preferred'))
                    self.__identical = True
            else:
                indexes_of_element = [0]
            outerHTML_input = re.findall(element_regex, formatted_element[0])
            outerHTML_input = re.findall(attr_regex, str(outerHTML_input))
            occurrences = [i for i, x in enumerate(self.__keys) if Counter(x[0]) == Counter(outerHTML_input)]
            self.__separate_classes_into_subclasses()
            if occurrences:
                for index_of_element in indexes_of_element:
                    row_index = occurrences[index_of_element]
                    self.__target = self.__keys[row_index]
                    self.__original_target = self.__target
                    rarity = 'Unique'
                    if self.__identical:
                        rarity = 'Duplicate'
                    type_of_element = 'html'
                    if self.__xml:
                        type_of_element = 'xml'
                    self.__print("\033[96m {}\033[00m".format(f'\u2B07 {rarity} Element '), newline=False)
                    self.__print("\033[92m {}\033[00m".format(f'{formatted_element[0][:24]}...>'), newline=False)
                    self.__print("\033[96m {}\033[00m".format(
                        f'with {type_of_element}-index -> ({row_index + 1} / {len(self.__keys)}) \u2B07'))
                    if element_xpath := self.__controller(self.__target):
                        program_return.append(element_xpath)
                    else:
                        self.__print('Xpath couldn\'t be found ...')
                        program_return.append(False)
                return program_return
            else:
                self.__print('Program couldn\'t find this element, make sure it is inputted correctly !')

        elif type(target) == int:
            if target <= len(self.__keys):
                self.__separate_classes_into_subclasses()
                self.__target = self.__keys[target - 1]
                self.__original_target = self.__target
                self.__print("\033[94m {}\033[00m".format(f'Index #{target}/{len(self.__keys)} | '), newline=False)
                if program_return := self.__controller(self.__target):
                    return program_return
                else:
                    self.__print('Xpath couldn\'t be found ...')
                    return False
            else:
                self.__print('Index surpasses total number of elements !')
                return False
        else:
            self.__print('Invalid Input or not proper element!')
            return False

    def __controller(self, target_elements):
        if unique_elements := self.__find_unique_elements(target_elements):
            if xpath := self.__find_xpath(unique_elements, target_elements):
                return xpath
        else:
            cut_down_elements = self.__select_attribute_pool_size(target_elements)
            target_elements = cut_down_elements
            if all_combinations := self.__find_combinations(target_elements):
                if indicators := self.__find_unique_combinations(all_combinations[0], all_combinations[1]):
                    if xpath := self.__find_xpath(indicators, target_elements):
                        return xpath
                else:
                    if not self.__child_method_ban:
                        if self.__child_method:
                            if result := self.__child_control(self.__target):
                                return result
                            else:
                                self.__child_method = False
                                self.__gen = []
                                target_elements = self.__original_target

                        if not self.__child_method:
                            return self.__checking_parent(target_elements)
                    else:
                        return self.__checking_parent(target_elements)
            else:
                return False

    def __format_html(self, input_html, format_override=False):
        parser = 'html.parser'
        if self.__xml:
            parser = 'xml'
        HTML = input_html
        if not format_override:
            if not self.__url_input:
                if '<' and '>' not in input_html:
                    try:
                        with open(input_html, 'r', encoding='utf-8', errors='ignore') as textfile:
                            HTML = textfile.read()
                    except FileNotFoundError:
                        self.__print('File Not Found !')
                    except OSError as o:
                        self.__print(o)
            else:
                HTML = requests.get(self.__dom).text
        formatted_HTML = HTML.splitlines()
        if not self.__pre_formatted:
            try:
                formatted_HTML = BeautifulSoup(HTML, parser).prettify().splitlines()
            except Exception as e:
                self.__print(e)
            if self.__xml:
                formatted_HTML.pop(0)

        return formatted_HTML

    def __process_html(self, formatted_HTML, element_regex, attr_regex, closing_tag_regex):
        index = 0
        for line in formatted_HTML:
            if re.match(closing_tag_regex, line.lstrip()):
                pass
            else:
                self.__formatted_html_lines.append(line.lstrip())
                elements = re.findall(element_regex, line)
                keys_of_element = re.findall(attr_regex, str(elements))
                if keys_of_element:
                    self.__keys.append([keys_of_element, len(line) - len(line.lstrip()), index])
                    index += 1

    def __regex_distributor(self, formatted_HTML):
        attr_regex = '(?:\w+[-.]*)+(?:=+\"[\w\d\s:;,$@#!\[\]^&?%\'*\\/+(){}.=-]*\")*'

        if self.__pre_formatted:
            for line in formatted_HTML:
                if '="' in line:
                    break
                elif "='" in line:
                    attr_regex = "(?:\w+[-.]*)+(?:=+\'[\w\d\s:;,$@#!\[\]^&?%\"*\\/+(){}.=-]*\')*"
                    break

        element_regex = '<.*?>'
        closing_tag_regex = '</.*?>'

        return element_regex, attr_regex, closing_tag_regex

    def __find_unique_elements(self, element):
        differences = []
        for keys in self.__keys:
            differences.append(set(element[0]) - set(keys[0]))
        differences.pop(element[2])
        unique_elements = list((differences[0]).intersection(*differences))
        if unique_elements:
            if not self.__show_all:
                if self.__no_digits:
                    for element in unique_elements:
                        if any(char.isdigit() for char in element):
                            unique_elements.remove(element)
                self.__identifier_method = 'element'
                if any('id="' in (fast_id := element) for element in unique_elements):
                    return fast_id
                elif unique_elements:
                    return min(unique_elements, key=len)
                else:
                    return False
            else:
                self.__identifier_method = 'element'
                return unique_elements
        else:
            return False

    @staticmethod
    def __find_combinations(elements):
        l_items = list(set(elements[0]))

        possible_indicators_pair = list(combinations(l_items, 2))
        if len(l_items) > 10:
            possible_indicators = possible_indicators_pair
        else:
            possible_indicators_three = list(combinations(l_items, 3))
            possible_indicators = possible_indicators_pair + possible_indicators_three

        return possible_indicators, elements

    def __find_unique_combinations(self, combinations_list, target_element):
        available_combinations = []
        for index, keys in enumerate(self.__keys):
            if index != target_element[2]:
                for comb in combinations_list:
                    if not set(comb).issubset(keys[0]):
                        available_combinations.append(comb)
        show_all = []
        for combination in combinations_list:
            pass_iter = False
            if available_combinations.count(combination) == len(self.__keys) - 1:
                if self.__no_digits:
                    for element in combination:
                        if any(char.isdigit() for char in element):
                            combinations_list.remove(combination)
                            pass_iter = True
                if not pass_iter:
                    self.__identifier_method = 'combination'
                    combination = [x for x in combination]
                    if not self.__show_all:
                        return combination
                    else:
                        show_all.append(combination)
                else:
                    pass

        return show_all

    def __select_attribute_pool_size(self, elements):
        if self.__speed == 'normal':
            speed = 25
        elif self.__speed == 'slow':
            speed = 35
        elif self.__speed == 'fast':
            speed = 15
        elif type(self.__speed) == int and int(self.__speed) <= 50:
            speed = self.__speed
        else:
            speed = 25
        return [elements[0][:speed], elements[1], elements[2]]

    def __format_xpath(self, unique_elements, all_elements):
        combination = False
        if self.__identifier_method == 'combination':
            combination = True

        child_index_xpath = ''
        parent_hierarchy = ''
        tag = all_elements[0][0]

        for child in reversed(self.__children_index):
            child_index_xpath += f'/*[{child}]'

        for _ in self.__gen:
            parent_hierarchy += f'/..'

        if not self.__show_all:
            unique_elements = [unique_elements]

        if not combination:
            for unique_element in unique_elements:
                if not self.__xml:
                    attr_type = (tag == unique_element)
                else:
                    attr_type = (tag in unique_element)
                if attr_type:
                    XPATH = f'//{tag}'
                    final_Xpath = XPATH + child_index_xpath + parent_hierarchy
                    self.__print(final_Xpath)
                    if not self.__show_all:
                        return final_Xpath
                else:
                    XPATH = f'//{tag}[@{unique_element}]'
                    final_Xpath = XPATH + child_index_xpath + parent_hierarchy
                    self.__print(final_Xpath)
                    self.__children_index = []
                    self.__gen = []
                    if not self.__show_all:
                        return final_Xpath
            return True
        elif combination:
            for unique_element in unique_elements:
                if classes := self.__merge_classes(unique_element):
                    unique_element = [x for x in unique_element if 'class="' not in x]
                    unique_element.append(classes)
                for element in unique_element:
                    if not self.__xml:
                        if tag == element:
                            unique_element.remove(element)
                    else:
                        if tag in element:
                            unique_element.remove(element)
                XPATH = f'//{tag}'
                for element in unique_element:
                    XPATH += f'[@{element}]'
                final_Xpath = XPATH + child_index_xpath + parent_hierarchy
                self.__print(final_Xpath)
                self.__children_index = []
                self.__gen = []
                if not self.__show_all:
                    return final_Xpath
            return True
        else:
            self.__print(f'Element\'s --{all_elements[0]}-- format is not normal !')
            return False

    def __find_xpath(self, unique_elements, target_elements):
        if result := self.__format_xpath(unique_elements, target_elements):
            self.__gen = []
            self.__children_index = []
            return result

    def __find_parent(self, element):
        target_index = element[2]
        child_index = 0
        for i in reversed(range(target_index)):
            if element[1] > self.__keys[i][1]:
                child_index += 1
                parent_element = self.__keys[i]
                return parent_element, child_index
            elif element[1] < self.__keys[i][1]:
                pass
            elif element[1] == self.__keys[i][1]:
                child_index += 1
            else:
                pass

    def __find_child(self, element):
        target_index = element[2] + 1
        generations = 0
        for i in range(len(self.__keys) - target_index):
            generations += 1
            if element[1] < self.__keys[i + target_index][1]:
                child_element = self.__keys[i + target_index]
                return child_element, generations
            elif element[1] > self.__keys[i + target_index][1]:
                return False
            elif element[1] == self.__keys[i + target_index][1]:
                return False
            else:
                pass

    def __parent_control(self, elements):
        if family := self.__find_parent(elements):
            target = family[0]
            self.__children_index.append(family[1])
            if result := self.__controller(target):
                return result
            else:
                return False
        else:
            return False

    def __child_control(self, elements):
        if family := self.__find_child(elements):
            self.__target = family[0]
            self.__gen.append(family[1])
            if result := self.__controller(self.__target):
                return result
            else:
                return False
        else:
            return False

    def __checking_parent(self, target_elements):
        if result := self.__parent_control(target_elements):
            self.__child_method = True
            return result
        else:
            self.__child_method = True
            return False

    def __separate_classes_into_subclasses(self):
        for keys in self.__keys:
            if has_classes := self.__check_classes(keys[0]):
                keys[0] = [x for x in keys[0] if 'class="' not in x]
                for classes in has_classes:
                    keys[0].append(f'class="{classes}"')

    @staticmethod
    def __check_classes(elements):
        regex = 'class=[\'\"].*?[\'\"]'
        classes = []
        for element in elements:
            if check := re.match(regex, element):
                values = check.string.split('"')
                if len(values) == 3:
                    classes.append(values[1].split())
                else:
                    pass
        if classes:
            return classes[0]
        else:
            return False

    @staticmethod
    def __merge_classes(unique_elements):
        class_merge = [x for x in unique_elements if 'class="' in x]
        if class_merge:
            combined_class = 'class="'
            for classes in class_merge:
                combined_class += classes[7:][:-1] + ' '
            combined_class = list(combined_class)
            combined_class[-1] = '"'
            combined_class = ''.join(combined_class)

            return combined_class
        return False

    def __print(self, text, newline=True):
        if self.__print_output:
            if newline:
                print(text)
            else:
                print(text, end='')
        else:
            pass
