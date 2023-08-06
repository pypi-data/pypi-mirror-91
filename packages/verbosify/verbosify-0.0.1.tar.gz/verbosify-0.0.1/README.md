# Verbosify

A cool function decorator to print selected comments 🎤

## A Simple Example

```py
from verbosify import verbosify, verbosify_with

@verbosify
def hello_word(uppercase=False):
    # This is the hello_word function
    if uppercase:
        # verbose: return hello word in uppercase
        return 'HELLO WORD'
    else:
        # verbose: return hello word in lowercase
        return 'hello word'

a = hello_word(verbose=True)
#> 'return hello word in lowercase'
print(a)
#> 'hello word'

a = hello_word(uppercase=True, verbose=True)
#> 'return hello word in uppercase'
print(a)
#> 'HELLO WORD'

a = hello_word()
print(a)
#> 'hello word'

a = hello_word(uppercase=True)
print(a)
#> 'HELLO WORD'
```


You can also choose which comments to print:

```py
@verbosify_with(' ')
def hello_word(uppercase=False):
    # This is the hello_word function
    if uppercase:
        # verbose: return hello word in uppercase
        return 'HELLO WORD'
    else:
        # verbose: return hello word in lowercase
        return 'hello word'

a = hello_word(verbose=True)
#> 'This is the hello_word function'
#> 'return hello word in lowercase'
print(a)
#> 'hello word'
```

