# XPanther
---     
        
<img src="https://user-images.githubusercontent.com/108073687/219871468-2fb5c446-dbb4-43eb-83c3-41d1f90c682d.jpg" width="500" height="300">

# Overview
------
## Find Unique Xpath expressions of HTML/XML elements.

### Mostly intended for Selenium and Appium automators.

- #### If you are a Web automator, check `XPantherIde App`, which is `XPantherIDE`, combined with GUI in a executable file, to ease your work.
- #### If you are an Appium automator, or want to find xpath of xml documents, check `XPanther`, which is part of xpanther package.


--------------
# Table of content:
- [XPantherIDE App](#xpantheride-app)
- [XPanther package](#xpanther-package)
    - [How to install](#how-to-install)
        - [XPanther](#x)
            - [How to use](#how-to-use-x)
            - [Options](#the-class-has-a-few-optional-parameters-that-you-can-change-to-modify-it-in-the-way-you-want)
        - [XPantherIDE](#xpantheride)
            - [How to use](#how-to-use-ide)
--------------
# XPantherIDE App
### `Download and install the window-based XPantherIDE application from Releases/XPanther Executable/Assets of this repository!`

### How to use:
- Open and run the executable file.
- Enter the url of the website, and click start!
- Start `right-clicking` over elements, and an alert pop-up will show their xpath
- When done, just close the browser.
- After closing, a output window will open, showing in a text file the output of the program, which are the xpath, the speed of xpath and language-specific Selenium code on how to find the elements.
--------------
# XPanther package
### This package contains 2 modules, `XPanther` and `XPantherIDE`

## How to install:
```python
pip install xpanther
```   
_or search it by `xpanther` if you have editor with package installer._

--------------
<a id="x"></a>
# XPanther

Import XPanther to your file like:
  
```python
from xpanther import XPanther
```
_If it doesn't show up (happens in pycharm sometimes), go to global site-packages (`pip show xpanther`<--cmd command to find directory), find and copy xpanther package, and paste it to your project's venv._

<a id="how-to-use-x"></a>
## How to use:

#### Insert inside **_XPanther()_** the whole **HTML/XML** text, which can be in the form of:
- **string**, 
- the **path** to any local text file you might have or 
- a page **url** (check below for optional-parameter page_url).

#### Insert inside **._capture()_** the **outerHTML/whole** text of element to be found:
- as a **string**
- or alternatively an **integer**, which represents the index of that element in the DOM, starting from 1 as the first.

```python
XPanther(dom).capture(element)
```

After writing this , run the code and the **xpath** of that element should be returned as value and printed in the console.

## Options:
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

### `For most optimal usage, keep this values as default, you have to only change  to xml=True if you are not dealing with HTML, and url_input=True if you like to fetch the HTML directly from link.`

--------------

# XPantherIDE

`XPantherIDE` is a simple Selenium script, that tries to mimic an IDE for finding xpaths instantly on any web page with just 1 click.

Import:
```python
from xpanther import XPantherIDE
```
Use:
```python
XPantherIDE('page_url').start()
```   
<a id="how-to-use-ide"></a>
## How to use:
    
#### After you run the program, the browser will open, and you can start finding xpaths by `right-clicking` over elements. A pop up alert will appear showing the xpath, you must accept/close the alert before trying again. You can then just close the browser and the program terminates correctly.
--------------

#### The program will test each xpath if it works, it is corresponding to clicked element, and output it in the console along with its speed.
--------------
--------------
### **Both programs are open to improvements or new ideas!**
-----------------------------------









