import glob

import json
char_index = {}
for name in glob.glob('*/*.txt'):
  print(name)
  b = open(name, 'rb').read()
  for ch in list(str(b)):
    if char_index.get(ch) is None:
      char_index[ch] = len(char_index)

open('char_index.json', 'w').write( json.dumps(char_index, indent=2, ensure_ascii=False) )
