# run whis :q
import glob

import os

for name in glob.glob('texts/*'):
  print(name)
  files = name.split('/').pop()
  text = os.popen('nkf -s {}'.format(name)).read()
  open('sjis/%s'%files, 'w').write(text)
