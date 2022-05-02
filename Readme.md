This project is an engine that allows beliefs management.

It is a python implementation of the AGM Belief Revision model.
This code base was based on the algorithms in Applications of Belief Revision by Mary-Anne Williams, 1996, and adapted from a MIT license: aima-python.

Authors: 
```
    Thomas HEBRARD - s212816
    Victor GUÉRIN - s212817
    Mohammed Zahed - s186517
    Viktor Anzhelev Tsanev - s184453
```

Installation: 

```bash
$ pip install -r requirements.txt
```

Run:

```
$ python hci.py
Select an action among these:

    r: Perform and AGM belief revision
    e: Empty knowledge base
    p: Print knowledge base
    m: Print all available actions

What do you want to do?: r
####  Let's perform a AGM Revision  ####
Please enter a logical formula:
>>> a>>b
Select an order between 0 and 1:
>>> 0.5
What do you want to do?: p
#### Here is your knowledge base:  ####
formula: b | ~a, order: 0.5
```
