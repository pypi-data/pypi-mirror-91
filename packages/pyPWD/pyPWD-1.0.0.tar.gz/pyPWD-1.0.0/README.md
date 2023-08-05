# pyPWD
A simple password generator

### Info
Passwords are generated in this format: (LETTERS) (SYMBOL) (NUMBERS)

### Usage: 
```python
import pyPWD
PyPWD.generate(letter_length, special_character, number_length)
```

### Example: 
simple code to generate 12 letters, a symbol, and 12 numbers

#### Code:
```python
import pyPWD

password = pyPWD.generate(12, '@', 12)
print(password)
```
you can also do 

```python 
from pyPWD import generate
``` 

to make it easier.

> Remember that instead of `pyPWD.generate()`, you should do `generate()`

#### Output:
This code will generate something like this:

```
OhvkpUYMUMaR@553339954271
```

in the format of LETTERS, then a SYMBOL, followed by a string of NUMBERS

### Inbuilt help feature
```python
import pyPWD

pyPWD.help()
```

Prints a short help message

### Credits
made by HYKANTUS.

🌐 [Website](http://hykantus.tk)

📺 [YouTube](https://www.youtube.com/channel/UCTrjOFWCDxorgDScilYH18Q)

📷 [InstaGram](https://www.instagram.com/hykantus/)

💻 [GitHub](https://github.com/HYKANTUS)
