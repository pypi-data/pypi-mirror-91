# **pushdit** 

## ***Installation***
```python
pip install pushdit
```


## ***Import***


```python
from pushdit import pushd, popd, pushit
```

## ***Features***
---
### **pushd**:
-   Tool that stores directories in a queue
-   <b>Directory path MUST EXIST </b> or *FileNotFoundError*
-   CWD will always be placed at the end of the queue
  
```python
import os

>>> pushd
- C:\Users\Antsthebul\Desktop\pushit;
>>> pushd('tests') 
>>> pushd
- C:\Users\Antsthebul\Desktop\pushit\tests;
0 tests
1 pushit
>>> os.getcwd()
'C:\\Users\\Antsthebul\\Desktop\\pushit\\tests'
```


Instead of having to use a seperate command to view CWD AND directory queue, `pushd` will echo the CWD as well as the directories that have been added to the queue. This is similar operation to the  `pushd` and `dirs` commands in *Linux*. The list of directories that `pushd` echoes, will be displayed in the order they were inserted, <b>0</b> being most recent. This is the order they will be *switched* to on default operation when using `pushit()` as a contenxtmanager, otherwise when calling `popd()`, will remove dir from back of queue. 

When `pushd` recives a *<..directory..>*, unless specified pushd will move program to that directory. See examples below.. 

## *Adding* to 'front' of queue *(Default)*
```python
>>> pushd
- C:\Users\Antsthebul\Desktop\pushit;
>>> pushd('tests/pushtest1')
>>> pushd
- C:\Users\Antsthebul\Desktop\pushit\tests\pushtest1;
0 pushtest1
1 pushit
```

### *Adding* to end of queue 
```python

>>> pushd
- C:\Users\Antsthebul\Desktop\pushit;

>>> pushd('tests/pushtest1', right=True)

>>> pushd
- C:\Users\Antsthebul\Desktop\pushit\tests\pushtest1;
0 pushit
1 pushtest1

>>> os.getcwd()
'C:\\Users\\Antsthebul\\Desktop\\pushit\\tests\\pushtest1'
```

## *Preventing* directory change
```python
>>> pushd('pushtest2', chdir=False) # was in tests\pushtest1 when called
>>> pushd
- C:\Users\Antsthebul\Desktop\pushit\tests\pushtest1;
0 pushtest2
1 pushit
2 pushtest1 
```
## *Clear* entire queue and return to inital location of call (cwd @ runtime)
```python
>>> pushd.clear() 
>>> pushd
- C:\Users\Antsthebul\Desktop\pushit;
```

## *Relative* paths ok!
```python
>>> pushd('tests/pushtest1/pushtest2')
>>> pushd
- C:\Users\Antsthebul\Desktop\pushit\tests\pushtest1\pushtest2;
0 pushtest2
1 pushit

>>> pushd('../..')
>>> pushd
- C:\Users\Antsthebul\Desktop\pushit\tests;
0 tests
1 pushtest2
2 pushit

```

## Even this...***thing***..
```python
>>> pushd
- C:\Users\Ansthebul\Desktop\pushit;
>>> pushd('~/documents') 
>>> pushd
- C:\Users\Ansthebul\documents;
0 documents
1 pushit
```
---
### **popd**
## *Remove* single directory from back of queue, like pop() 
```python
>>> pushd('pushtest2', chdir=False)
>>> popd()
'C:\\Users\\Antsthbul\\pushit\\tests\\pushtest1'
>>> pushd
- C:\Users\Antsthebul\Desktop\pushit\tests\pushtest1;
0 pushtest2
1 pushit
```
## *Specify* directory to be removed
    
-   *Feature unavailable*
---
### **pushit** 
>Where it all comes together..

## *no args*
-   The *pushd queue* **must** be populated

```python
>>> pushd('tests', chdir=False)
>>> pushd('tests/pushtest1', chdir=False) 
>>> pushd('tests/pushtest1/pushtest2', chdir=False) 
>>> pushd()
>>> pushd
- C:\Users\Antsthebul\Desktop\\pushit;
0 pushtest2
1 pushtest1
2 tests
3 pushit

>>> with pushit() as lvl1:
...    print('Do stuff here')
...    print(os.getcwd())
...    print()
...    with pushit() as lvl2:
...        print('Do more stuff here')
...        print(os.getcwd())
...        print()
...        with pushit() as lvl3:
...            print('OK i think you get the idea')
...            print(os.getcwd())
...            print()
...        print('Back in lvl2')
...        print(lvl2)
...    print('inside lvl1')
...    print(lvl1)



Do stuff here
C:\Users\Antsthebul\Desktop\pushit\tests\pushtest1\pushtest2

Do more stuff here
C:\Users\Ansthebul\Desktop\pushit\tests\pushtest1

OK i think you get the idea
C:\Users\Ansthebul\Desktop\pushit\tests

Back in lvl2
- C:\Users\Ansthebul\Desktop\pushit\tests\pushtest1;

inside lvl1
- C:\Users\Ansthebul\Desktop\pushit\tests\pushtest1\pushtest2;
0 pushit

>>> pushd
- C:\Users\Ansthebul\Desktop\pushit;
0 pushit

>>> os.getcwd()
C:\Users\Antsthebul\Desktop\pushit
```
## *with args*
```python
>>> pushd
- C:\Users\Antsthebul\Desktop\\pushit;
>>> with pushit('tests/pushtest1/pushest2'):
...     print(os.getcwd())
C:\Users\Antsthebul\Desktop\pushit\tests\pushtest1\pushtest2
>>> os.getcwd()
'C:\\Users\\Antsthebul\\Desktop\\pushit'
```
