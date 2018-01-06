# run whis :q
import glob

import os

for name in glob.glob('texts/*'):
  print(name)
  files = name.split('/').pop()
  text = os.popen('nkf -e {}'.format(name)).read()
  open('eucs/%s'%files, 'w').write(text)
