#pip3 install replit
from replit.database.database import Database

class Connection:
  def __init__(self,db_url):
    self.db=Database(db_url=db_url)
  def send(self,value):
    value = [value[i:i+1000000] for i in range(0,len(value),1000000)]
    for i in value:
      self.db['conn-DATA'] = i
      self.db['conn-stat'] = 'data'
      while self.db['conn-stat'] != 'done':
        pass
    self.db['conn-stat'] = 'end'
    del self.db['conn-DATA']
  def recv(self):
    r = b''
    while not a in db:
      pass
    while db['conn-stat'] != 'end':
      if db['conn-stat'] == 'data':
        r += db['conn-DATA']
        db['conn-stat'] = 'done'

if __name__ == '__main__':
  from sys import argv
  from os import environ
  from os.path import exists
  
  usage=f'usage: {argv[0]} [db_url] (post|get) <file>\n    If [db_url] is not specified, use $REPLIT_DB_URL instead.\n\n    post - Send file <file>.\n    get  - Recivive file. If nobody sends, wait for sending.'
  
  if len(argv) == 2 and (argv[1] == '--help'):
    print(usage)
  
  if 'REPLIT_DB_URL' in environ and (len(argv) == 3):
    conn = Connection(environ['REPLIT_DB_URL'])
    do = argv[1]
    filename = argv[2]
  elif len(argv) == 4:
    conn = Connection(argv[1])
    do = argv[2]
    filename = argv[3]
  else:
    print(usage)
    print('Note: check $REPLIT_DB_URL.')
  
  if not exists(filename):
    print(f"Error: '{filename}' doesn't exists")
    exit(1)
  
  if do == 'post':
    with open(filename, 'rb') as f:
      conn.send(f.read())
  elif do == 'get':
    with open(filename, 'wb') as f:
      f.write(conn.recv())
