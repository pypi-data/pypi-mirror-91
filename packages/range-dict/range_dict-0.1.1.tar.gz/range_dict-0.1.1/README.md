### RangeDict 
Ranges are omnipresent in our lives - we are talking about durations, lengths or intervals. 
Unfortunately they are hard to model in code using standard data structures built in mainstream languages.

This library offers you fast `range dict` implementation, built on top of Python's standard dictionary.  

#### Documentation
https://github.com/logx/range-dict/wiki/Documentation

#### Example usage

```python
>>> holidays = RangeDict()

>>> holidays = RangeDict({(date(2020, 7, 1), date(2020, 7, 14)): "John's holidays"})

>>> holidays[date(2020, 7, 1), date(2020, 7, 14)] = "John's holidays"

>>> holidays[date(2020, 7, 10)]
["John's holidays"]

>>> holidays[date(2020, 7, 10), date(2020, 7, 20)] = "Mary's holidays"

>>> holidays[date(2020, 7, 10)]
["John's holidays", "Mary's holidays"]
```

#### Supported data types
Range can be expressed using:
 - int
 - float
 - date
 - datetime
 - any other object that implements `__eq__` method

#### Standard behavior
Because `RangeDict` extends Python's standard dictionary,
it is capable of accepting single value as a key:

```python
>>> holidays[date(2020, 7, 12)] = "Piotr's (one day) holiday"
```

#### Installation
Library can be installed directly from GitHub using `pip`:
```
pip install git+git://github.com/logx/range-dict.git@0.0.1
```
Remember to replace `0.0.1` with actual version from [releases](https://github.com/logx/range-dict/releases). 
Or skip `@0.0.1` to install the most recent version.

