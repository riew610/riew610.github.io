import websocket, json, time, requests
import hashlib, jwt, uuid
from urllib.parse import urlencode

try:
  import thread
exceept ImportError:
  import _thread as thread
  
price = 300

def on_message(ws, message):
  json_data = json.loads(message)
  global price
  percent = (price - json_data['trade_price']) / json_data['trede_price'] * 100
  print(percent)
  print('시작 가격보다 ', percent, '변화')
  if percent > 0.1:
    query = {
      'market' : 'KRW-ETH',
      'side' : 'ask',
      'volume' : '0.0015',
      'price' : json_data['trade_price'],
      'ord_type': 'limit',
    }
    
    query_string = urlencode(query).encode()
    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()
    
    payload = {
      'access_key' : API_KEY,
      'nounce': str(uuid.uuid4()),
      'query_hash' : query_hash,
      'query_hash_alg' : 'SHA512',
    }
    
    jwt_token = jwt.encode(payload, SECRET_KEY).decode('utf-8')
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {'Authorization': authorize_token}
    res = requests.post('https://api.upbit.com/v1/orders', params = query, headers = headers)
    print(res.json())
  elif percent < -0.1:
    query = {
      'market' : 'KRW-ETH',
      'side' : 'ask',
      'volume' : '0.0015',
      'price' : json_data['trade_price'],
      'ord_type': 'limit',
    }
    
    query_string = urlencode(query).encode()
    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()
    
    payload = {
      'access_key' : API_KEY,
      'nounce': str(uuid.uuid4()),
      'query_hash' : query_hash,
      'query_hash_alg' : 'SHA512',
    }
    
    jwt_token = jwt.encode(payload, SECRET_KEY).decode('utf-8')
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {'Authorization': authorize_token}
    res = requests.post('https://api.upbit.com/v1/orders', params = query, headers = headers)
    print(res.json())
    
def on_error(ws,error):
  print(error)
  
def on_close(ws):
  print('### closed ###')

def on_open(ws):
  def run(*args):
    ws.send(json.dumps(
      [{'ticket':'test'},{'type':'ticker','codes':['KRW-ETH']}]))
  thread.start_new_thread(run,())
  
websocket.enableTrace(True)
ws = websocket.WebSocketApp('wss://api.upbit.com/websocket/v1',
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close)
ws.on_open = on_open
print(ws.on_open)
ws.run_forever()
