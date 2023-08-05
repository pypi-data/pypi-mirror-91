def table(extend=False):
  if extend:
    TABLE = {
      "I":1,
      "IV":4,
      "V":5,
      "IX":9,
      "X":10,
      "XL":40,
      "L":50,
      "XC":90,
      "C":100,
      "CD":400,
      "D":500,
      "CM":900,
      "M":1000,
      "I̅V̅":4000,
      "V̅":5000,
      "I̅X̅":5000,
      "I̅X̅":9000,
      "X̅":10000,
      "X̅L̅":40000,
      "L̅":50000,
      "X̅C̅":90000,
      "C̅":100000,
      "C̅D̅":400000,
      "D̅":500000,
      "C̅M̅":900000,
      "M̅":1000000,
    }
  else:
    TABLE = {
      "I":1,
      "IV":4,
      "V":5,
      "IX":9,
      "X":10,
      "XL":40,
      "L":50,
      "XC":90,
      "C":100,
      "CD":400,
      "D":500,
      "CM":900,
      "M":1000,
  }
  return TABLE

def roman(num:int,extend=False):
  if not num: return 'N'
  pos = [(r,v) for r,v in table(extend).items()]
  rom = ""
  index = -1
  while num!=0:
    if num >= pos[index][1]:
      t = num//pos[index][1]
      rom += (pos[index][0] * t)
      num -= (pos[index][1] * t)
    index -= 1
  return rom

def roman_range(*args,extend=False):
  if len(args)==1:
    start, stop, step = 0, args[0], 1
  if len(args)==2:
    start, stop, step = args[0], args[1], 1
  if len(args)==3:
    start, stop, step = args[0], args[1], args[2]
  i = start
  while i < stop:
    yield rom(i, extend)
    i+=step  

def number(rom:str):
  extend = '̅' in rom
  if not rom or rom=='N': return 0
  lis = [(table(extend)[r] if r in table(extend) else 'mul') for r in rom]
  num = 0
  for i in range(0,len(lis)-1):
    if lis[i+1]=='mul':
      lis[i]*=1000
      lis[i+1] = 0
    if lis[i]>=lis[i+1]:
      num+=lis[i]
    else:
      num-=lis[i]
  num+=lis[-1]
  return num

class rom:
  def __init__(self,n:int,extend=False):
    if type(n)==str:
      n = number(n)
    if n < 0: raise ValueError("Roman number should greater than 0")
    self.val = int(n)
    self.extend = extend
  
  def __repr__(self):
    return roman(self.val,self.extend)

  def __add__(self, other):
    if type(other)==int: return rom(self.val + other,self.extend or other.extend)
    return rom(self.val + other.val,self.extend or other.extend)

  def __sub__(self, other):
    if type(other)==int: return rom(self.val - other,self.extend or other.extend)
    return rom(self.val - other.val,self.extend or other.extend)

  def __mul__(self, other):
    if type(other)==int: return rom(self.val * other,self.extend or other.extend)
    return rom(self.val * other.val,self.extend or other.extend)

  def __eq__(self, other):
    if type(other)==int: return self.val==other
    return self.val == other.val

  def __ne__(self, other):
    return self.val != other.val
  
  def __gt__(self, other):
    if type(other)==int: return self.val>other
    return self.val > other.val

  def __ge__(self, other):
    if type(other)==int: return self.val>=other
    return self.val >= other.val

  def __lt__(self, other):
    if type(other)==int: return self.val<other
    return self.val < other.val

  def __le__(self, other):
    if type(other)==int: return self.val<=other
    return self.val <= other.val

  def __int__(self):
    return self.val

if __name__=="__main__":
  for i in range(4000):
    if (i!=number(roman(i))):
      print("Error at", i)
      break
  print("No Error")