# XPanther

## Find Unique Xpath expressions of HTML/XML elements.

### This python module's objective is to find unique xpath selector for any element in a document, using unique attributes/combination of attributes/parent or child relationship methods to find and write such expression for correctly identifying that element.

## How to install:
    
    pip install xpanther
    
or search it by 'xpanther' if you have editor with package installer.

Then, import it to your file like:
  
    from xpanther.XPanther import XPanther

#### It comes with two classes, the 1st, main one -- XPanther(), and the 2nd one which I'll explain later, XPantherIDE().

### **XPanther()** class needs to take as parameter the whole **DOM/HTML/XML** text, which can be in the form of **string**, the **path** to any local text file you might have or a page **url** (check below for optional-parameter page_url).

This class has only one intended function to be used, which is **capture()**.

### XPanther('//testFile.txt').capture() -- this function takes as parameter the **outerHTML/whole** text of element to be found, or alternatively an integer, which represents the index of that element in the DOM, starting from 1 as the first (check below for interesting usage of index input).

After writing this , run the code and the **xpath** of that element should be returned and printed in the output

#### Code execution illustration:

    #INPUT
    XPanther('//testFile.txt').capture('<li class="stepper-item align-items-center flex-nowrap" aria-current="step">')
    
    #OUTPUT
    ⬇ Element with html-index -> (945 / 1088) ⬇
    //li[@aria-current="step"][@class="flex-nowrap"]
    
    
    
#### **The class has a few optional-parameters that you can change to modify it in the way you want:**

-**xml**, default is False, you MUST set it to True if document is not HTML, this is because the xml document can contain uppercase characters in attributes, unlike html, so a different parser needs to be used.

-**pre_formatted**, default is False, you can set it to True if you have already formatted document and don't want formatter of XPanther to change anything.

-**url_input**, default is False, should set to True if you intend to insert page url intead of text or file as the dom parameter of this class.

-**child_method**, default is True, you can set it to False if you don't want the Xpath to be found using its children, reason for this can depend on context.

-**print_output**, default is True, you might set it to False if you don't want the program to print anything in console but just return the xpath as a value in any variable or function.

-**speed**, default is 'normal', other valid options are 'fast' -- (less detailed, faster execution), 'slow' -- (more detailed, slower execution), or an integer (maximum is 50,which represent the number of attributes of element program can take and proccess to find combinations of).
          'slow' can take as much as 35 attributes of element to go on and find combinations of, it is my recommended maximum limit, any more than that might crash the computer.
          if you have a slow computer, better set it to 'fast', cause it takes lesser number of combination and lowers memory and performance consumption, thus increasing speed of execution.

### For most optimal usage, keep this values as default, you have to only change  to xml=True if you are not dealing with HTML, and url_input=True if you like to fetch the HTML directly from link. 

#### Interesting way which you can utilize putting an integer as parameter to capture(), is this function like here:

      for x in range(100):
          XPanther('xpath_test.txt').capture(x+1)

Literally, create and write an unique xpath for every element in the document if you want (change the number in range() accordingly).


## If you are into web automation, that's where **XPantherIDE** comes into play.

XPantherIDE is a simple script, which opens a chrome browser on your preferred starting page url, and will register any click made in the page, after you close the browser as you normally would, every unique xpath of element you clicked upon will be shown in succession, thus making automation a lot easier, especially for people who struggle finding xpaths.

Import:
    
    from xpanther.XPantherIDE import XPantherIDE

--**DISCLAIMER**-- This script is still experimental, buttons that can redirect the page don't return value for the moment, this is a bug that will be fixed in the future.

**Both programs are open to improvements or new ideas.**










