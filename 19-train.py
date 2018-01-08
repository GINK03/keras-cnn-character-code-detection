import pickle
import gzip
import numpy as np
import random
import os
import sys
import statistics
import glob
import re
import json
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model, load_model
from keras.layers import Lambda, Input, Activation, Dropout, Flatten, Dense, Reshape, merge
from keras.layers import Concatenate, Multiply, Conv1D, MaxPool1D, BatchNormalization
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator
from keras.layers.normalization import BatchNormalization as BN
from keras.layers.core import Dropout
from keras.optimizers import SGD, Adam
from keras import backend as K

def CBRD(inputs, filters=64, kernel_size=3, droprate=0.5):
  x = Conv1D(filters, kernel_size, padding='same',
            kernel_initializer='random_normal')(inputs)
  x = BatchNormalization()(x)
  x = Activation('relu')(x)
  return x


def DBRD(inputs, units=4096, droprate=0.35):
  x = Dense(units)(inputs)
  x = BatchNormalization()(x)
  x = Activation('relu')(x)
  x = Dropout(droprate)(x)
  return x

input_tensor = Input( shape=(300, 95) )

x = input_tensor
x = CBRD(x, 2)
x = CBRD(x, 2)
x = MaxPool1D()(x)

x = CBRD(x, 4)
x = CBRD(x, 4)
x = MaxPool1D()(x)

x = CBRD(x, 8)
x = CBRD(x, 8)
x = MaxPool1D()(x)

x = CBRD(x, 16)
x = CBRD(x, 16)
x = CBRD(x, 16)
x = MaxPool1D()(x)

x = CBRD(x, 32)
x = CBRD(x, 32)
x = CBRD(x, 32)
x = MaxPool1D()(x)

x = Flatten()(x)
x = Dense(3, name='dense_last', activation='sigmoid')(x)
model = Model(inputs=input_tensor, outputs=x)
model.compile(loss='binary_crossentropy', optimizer='adam')

import dbm
import plyvel
if '--train' in sys.argv:
  init = 0
  try:
    target_model = sorted(glob.glob('models/*.h5'))[-1]
    model.load_weights( target_model ) 
    init = int( re.search(r'/(\d{1,}).h5', target_model).group(1) )
    print('init state update', init)
  except Exception as e:
    print(e)
 
  db = plyvel.DB('key_data.ldb')
  keys = [ key for key, val in db ]
  for i in range(200):
    Xs, ys = [], []
    for key in random.sample(keys, 500):
      X, y = pickle.loads( db.get(key) )
      Xs.append(X); ys.append(y)
    Xs, ys = np.array(Xs), np.array(ys)
    #print(Xs)
    model.fit(Xs, ys, epochs=2, batch_size=32)
    if i%5 == 0:
      model.save_weights('models/{:09d}.h5'.format(i))

if '--predict' in sys.argv:
  char_index = json.loads( open('./char_index.json').read() ) 

  name = [ arg.split('=').pop() for arg in sys.argv if '--file' in arg ].pop()
  print(name)
  b = open(name, 'rb').read()

  arr = []
  for ch in list(str(b)):
    arr.append( char_index[ch] )
  
  base = [ [0.0]*len(char_index) for i in range(300) ]
  for i in range(100):
    index = arr[i]
    base[i][index]  = 1.0
  
  X = np.array([ base ])
  model.load_weights( sorted(glob.glob('models/*.h5')).pop() )
  y = model.predict(X).tolist().pop()
  p = np.argmax(y)
  if p == 0:
    print('this document is EUC.')
  elif p == 1:
    print('this document is SJIS')
  elif p == 2:
    print('this document is UTF8')
    
