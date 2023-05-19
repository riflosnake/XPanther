# XPanther
        
        
<img src="https://user-images.githubusercontent.com/108073687/219871468-2fb5c446-dbb4-43eb-83c3-41d1f90c682d.jpg" width="500" height="300">

## Find Unique Xpath expressions of HTML/XML elements.

### Mostly intended for Selenium and Appium automators.

### This python module's objective is to find unique xpath selector for any element in a document, using unique attributes/combination of attributes/parent or child relationship methods to find and write such expression for correctly identifying that element.

## How to install:
```python
pip install xpanther
```   
_or search it by `xpanther` if you have editor with package installer. If it doesn't show up (happens in pycharm sometimes), go to global site-packages (`pip show xpanther`<--cmd command to find directory), find and copy xpanther package, and paste it to your project's venv._

## This package contains 2 modules, `XPanther` and `XPantherIDE`, let's start with the powerhouse!
Import XPanther to your file like:
  
```python
from xpanther import XPanther
```


## How to use:

#### Insert inside **_XPanther()_** the whole **HTML/XML** text, which can be in the form of:
- **string**, 
- the **path** to any local text file you might have or 
- a page **url** (check below for optional-parameter page_url).

#### Insert inside **._capture()_** the **outerHTML/whole** text of element to be found:
- as a **string**
- or alternatively an **integer**, which represents the index of that element in the DOM, starting from 1 as the first (check below for interesting usage of index input).

```python
XPanther(dom).capture(element)
```

After writing this , run the code and the **xpath** of that element should be returned as value and printed in the console.

#### Code execution illustrations:

<img src="https://user-images.githubusercontent.com/108073687/219906727-07172ca3-b5e9-4170-9538-9d0c777fb4c5.jpg" width="900">
<img src="https://user-images.githubusercontent.com/108073687/219906731-d7215aab-1526-440f-809a-f14c6f3b31ab.jpg" width="900">
    
#### **The class has a few optional-parameters that you can change to modify it in the way you want:**

- `xml` (default: `False`): Set this to `True` if document is not HTML, this is because the xml document can contain uppercase characters in attributes, unlike html, so a different parser needs to be used.

- `pre_formatted` (default: `False`): Set this to `True` if you have already formatted document and don't want formatter of XPanther to change anything.

- `url_input` (default: `False`): Set this to `True` if you intend to insert page url intead of text or file as the dom parameter of this class.

- `child_method` (default: `True`): Set this to `False` if you don't want the Xpath to be found using its children, reason for this can depend on context.

- `show_all` (default: `False`): Set this to `True` if you want all possible working xpaths found and not resort to only the one chosen by program.

- `no_digits` (default: `False`): Set this to `True` if you don't want element attributes that contain numbers.

- `print_output` (default: `True`): Set this to `False` if you don't want the program to print anything in console but just return the xpath as a value in any variable or function.

- `speed`  (default: `'normal'`): other valid options are `'fast'` -- (less detailed, faster execution), `'slow'` -- (more detailed, slower execution), or an integer (maximum is 50, which represent the number of attributes of element program can take and proccess to find combinations of).
          if you have a slow computer, better set it to 'fast', cause it takes lesser number of combination and lowers memory and performance consumption, thus increasing speed of execution.

### For most optimal usage, keep this values as default, you have to only change  to xml=True if you are not dealing with HTML, and url_input=True if you like to fetch the HTML directly from link. 


#### Interesting way which you can utilize putting an integer as parameter to capture(), is this function like here:
```python
for x in range(100):
    XPanther('xpath_test.txt').capture(x+1)
```
Literally, create and write an unique xpath for every element in the document if you want (change the number in range() accordingly).



# If you are into web automation, that's where `XPantherIDE` comes into play.

`XPantherIDE` is a simple Selenium script, that tries to mimic an IDE for finding xpaths instantly on any web page with just 1 click.

Import:
```python
from xpanther import XPantherIDE
```
Use:
```python
XPantherIDE('page_url').start()
```   
    
#### After you run the program, the browser will open, and you can start finding xpaths by `right-clicking` over elements. A pop up alert will appear showing the xpath, you must accept/close the pop up before trying again.

### **Both programs are open to improvements or new ideas!**










