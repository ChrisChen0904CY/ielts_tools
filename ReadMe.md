# ielts_tools version 1.0
---
**Author:**&nbsp;&nbsp;***Chris Chen***

**Contact:**&nbsp;&nbsp;***chrischanyedu@gmail.com***

**Github:**&nbsp;&nbsp;***https://github.com/ChrisChen0904CY***

**Release Date:**&nbsp;&nbsp;***8/25/2023***

# Brief Introduction
---
## What's this for
---
This package is designed to aid ***IELTS exam*** preparation, with a specific focus on ***enhancing dictation skills*** and ***expanding vocabulary***.

## How this work
---
You can include words that ***are frequently misspelled***, ***lead to confusion while listening***, or ***prove challenging to comprehend*** in the list files. Subsequently, you can run the `main.py` file provided in this context.

Then you have the option to select either a `'dictation'` or a `'reading test'` as illustrated below:

![](./imgs/1.png)
![](./imgs/2.png)

Here's an instance for the ***reading test***:

![](./imgs/3.png)
![](./imgs/4.png)

## Basement
---
The entire project, or rather, the package, relies on the utilization of the ***youdao API***. Consequently, this package may become non-functional when the youdao API be discontinued.

# Related File Structure
---
To ensure the program can run correctly, it is advisable to structure your files as follows:

├─audios
│  ├─UK
│  └─US
├─dictation_list.txt
├─read_list.txt
├─meanings.txt
├─ielts_tools.py
├─main.py

# Revelant Packages
---
To ensure this package functions as intended, you should verify whether you have installed the following packages:
> urlib
> json
> playsound

If not, you can copy the respective command here for installation:

**1. urlib**
```python
pip install urlib
```

**2. json**
```python
pip install json
```

**3. playsound**
```python
pip install playsound
```

# How to Use
---
Here is ***the most significant section*** of this file. Perhaps you navigated directly to this part upon opening the file. While it is easily understandable, you may overlook some intriguing terms along the way.

## Statement of the core Class
---
As you can observe, the sole component within this package is a class named ***WordTrainer***. Much like its namesake, isn't it?

Alright, let me walk you through the core components step by step:

### Initialize
---
You can never prepare a meal without a pot, can you? Similarly, if you wish to utilize this for exercises, you must initialize it as follows:

```python
UK_Trainer = WordTrainer(1)
```

It specifies that you create an object with an ***English Accent***, which is commonly used in IELTS.

The only parameter you can provide during initialization is either the number *0* or *1*. *0* corresponds to an ***American Accent***, while *1* corresponds to an ***English Accent***.

### Dictation Function
---
After initializing an object, you can invoke the dictation function to undergo a personalized dictation, as illustrated below (assuming your object is named *UK_Trainer*):

```python
# 10 here refers to the batch size of the test and can be any positive number you like
UK_Trainer.dic_test(10)
```

***Tips.*** There are certain audio segments that cannot be played, and for these words, you do not need to spell them; they will be skipped as the follwing:

![](./imgs/5.png)

### Reading-Test Function
---
After initializing an object, you can invoke the dictation function to undergo a personalized read test, as illustrated below (assuming your object is named *UK_Trainer*):

```python
# 10 here refers to the batch size of the test and can be any positive number you like
UK_Trainer.unknow_test(10)
```
### Inquire about a Word Quickly
---
You can also simply request the definition of a specific word using this method:

```python
# good here can be replaced to any word you want to ask
UK_Trainer.showInfo('good')
```
***Tips.*** When the word you inquire about is not found in the current file, it will be downloaded to the ***read_list.txt***, and its definitions will be printed.

## Deal with Phrases
---
When you need to request the meaning of a phrase or add a phrase to your list, you ***must*** replace the ***spaces*** between words with a plus symbol +.

Here's an instance for you:

The phrase `"pin down"` should be written as `"pin+down"`.

![](./imgs/6.png)

**`However, you should disregard this rule when participating in dictation exercises. For instance, you should simply type 'pin down' when you hear it insteadd of 'pin+down'.`**

# Easily Use
---
If you prefer a quick and convenient use of this package, you can just run the code provided below, and you will obtain the same results I have demonstrated above:

```python
from ielts_tools import WordTrainer


if __name__ == "__main__":
    # Training based on UK accent
    UK_Trainer = WordTrainer(1)
    # Choose the test mode
    # 0 -- Dictation mode
    # 1 -- Reading test mode [i.e. training by typing the correct meaning of the word]
    mode = input('Would you like a dictation or a reading-test?\n[Type 0 for the former and 1 for the latter]\n> ')
    mode = eval(mode)
    print('OK! Now please set the batch size u\'d like to take: ')
    batch_size = eval(input('> '))
    # Start the test here
    if mode == 0:
        UK_Trainer.dic_test(batch_size)
    elif mode == 1:
        UK_Trainer.unknow_test(batch_size)
    else:
        # When type an unexpected mode, log the information
        print("There's something wrong in the mode settings")
```

# Thanks
---
Here, I would like to extend my heartfelt ***gratitude*** to ***Kristine Cheng***, who has been with me throughout the entire process of developing this package and has provided me with immense support and encouragement. By the way, she's not only my ***girlfriend*** but also ***the most amazing girl*** I've ever met.