import dbm
import pickle
db = dbm.open('14-text.dbm', 'c')

for index, key in enumerate(db.keys()):
  val = pickle.loads(db[key])
  title = val['titles']
  body = val['bodies']
  print(title) 
  try:
    open('texts/{:09d}.txt'.format(index), 'w').write( title + '\n' + body )
  except OSError as ex:
    print(ex)
    ...
