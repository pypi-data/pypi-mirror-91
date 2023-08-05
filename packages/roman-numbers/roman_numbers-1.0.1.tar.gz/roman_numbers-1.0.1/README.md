# Roman numerals

Manage roman numerals using roman number object.

## Convert roman numeral to integers

* **`roman` function**

return roman numeral string

```python
import roman_numbers as r

x = 10
print(r.roman(x))
```
Output:
```python
>> X
```

* **`number` function**

return integers from roman numeral

```python
import roman_numbers as r

x = 'X'
print(r.number(x))
```
Output:
```python
>> 10
```

* **`rom` object**

support Basic and Compare opeartion for roman numeral
```python
from roman_numbers import rom

>> rom(10) + rom(10) # add
>> XX

>> rom(5) - rom(1) # sub
>> IV

>> rom(5) * 3 # mul
>> XV

>> rom('V') > rom('XI') # compare
>> False

>> rom('V') == 5 # compare
>> True

>> int(rom('XI'))
>> 11
```