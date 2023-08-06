# **PY2HTML**

## **Introduction**

### **What is PY2HTML?**

PY2HTML is a python module that creates static websites using python

### 


### **How to Install:**

#### **Windows:**

```
pip install py2html
```

#### **Linux/Mac**
```
sudo pip3 install py2html
```


## **Hello World Example:**

```python
from py2html.main import *

page = web() # Creating object to receive web class

page.create(title='My Site') # Creating website and defining title

page.label(text='Hello World') # Creating Label

page.compile() # Create html page, return: page.html
```


## **How to contribute**

You can contribute in the following ways:

- Helping in the creation of the library

- Disclosing the project

Open an issue explaining how you can contribute to the project and show what you did for the project (class, function, incrementing a function)!


## **How to learn?**

- [Documentation](https://github.com/andreluispy/py2html/tree/main/doc's)
- GitHub issues
- **Python Help:**
    ```python
    help(web) #help from class and functions!
    ```
