import glob

import json

import pickle

import dbm

import hashlib

db = dbm.open('key_data.dbm', 'c')

char_index = json.loads( open('./char_index.json').read() )

for name in glob.glob('eucs/*.txt'):
  b = open(name, 'rb').read()

  arr = []
  for ch in list(str(b)):
    arr.append( char_index[ch] )
  
  base = [ [0.0]*len(char_index) for i in range(300) ]
  for i in range(100):
    index = arr[i]
    base[i][index]  = 1.0
  
  X = base
  y = [1, 0, 0]
 
  val = pickle.dumps((X,y))
  key = hashlib.sha256(val).hexdigest()
  print(key)
  db[key] = val

for name in glob.glob('sjis/*.txt'):
  b = open(name, 'rb').read()

  arr = []
  for ch in list(str(b)):
    arr.append( char_index[ch] )
  
  base = [ [0.0]*len(char_index) for i in range(300) ]
  for i in range(100):
    index = arr[i]
    base[i][index]  = 1.0
  
  X = base
  y = [0, 1, 0]
 
  val = pickle.dumps((X,y))
  key = hashlib.sha256(val).hexdigest()
  print(key)
  db[key] = val

for name in glob.glob('texts/*.txt'):
  b = open(name, 'rb').read()

  arr = []
  for ch in list(str(b)):
    arr.append( char_index[ch] )
  
  base = [ [0.0]*len(char_index) for i in range(300) ]
  for i in range(100):
    index = arr[i]
    base[i][index]  = 1.0
  
  X = base
  y = [0, 0, 1]
 
  val = pickle.dumps((X,y))
  key = hashlib.sha256(val).hexdigest()
  print(key)
  db[key] = val
