#coding=utf-8
# __all__=['N','HTTPServer']
import sys
# from .. import py#ValueError: Attempted relative import in non-package
if __name__.endswith('qgb.N'):from .. import py
else:import py


gError=[]
def setErr(ae):
	py.importU()
	global gError
	if U.gbLogErr:# U.
		if type(gError) is list:gError.append(ae)
		elif gError:gError=[gError,ae]
		else:gError=[ae]
	else:
		gError=ae
	if U.gbPrintErr:U.pln('#Error ',ae) # U.

#if 'qgb.U' in sys.modules:U=sys.modules['qgb.U']
#elif 'U' in sys.modules:  U=sys.modules['U']
#else:
#	try:
#		# from sys import path as _p
#		# _p.insert(-1,_p[0][:-1-1-3-1]) # python2.7\\qgb\\N
#		# from qgb import U
#		# if U.iswin():from qgb import Win
#		sys.path.insert(0,'..')
#		import py
#		import U,Win
#	except Exception as e:
#		U.pln( e)
#		Win=py.Class()
#		Win.isxp=lambda:0		
#		gError.append(e)
#try:py=U.py
#except Exception as e:gError.append(e)
try:
	if __name__.endswith('qgb.N'):
		from . import HTTP
		from . import HTTPServer
	else:
		import HTTP
		import HTTPServer
except Exception as ei:
	py.traceback(ei)
	# py.importU().repl()
	# py.pdb()
	# raise ei
# import HTTPServer
# import HTTP
	
def findFunc(name,root=9,depth=3,case=False):
	U.pln( dir(root)       )
	U.pln( '='*44          )
	U.pln( globals().keys())
	U.pln( '='*44          )
	U.pln( locals().keys() )
	U.pln( '='*44          )
	U.pln( vars().keys()   )
	exit()
# findFunc('set*')		
	
def get(url,protocol='http',file=''):
	py.importU()
	T=U.T
	if '://' in url:
		p=T.sub(url,'',':')
		if p:protocol=p
		else:raise U.ArgsErr(url)
	else:url=protocol+'://'+url
	if url.startswith('http'):
		# import HTTP
		return HTTP.get(url,file=file)	
	raise U.NotImplementedError
	return U.getAllMods()

def http(url,method='get',*args):
	return HTTP.method(url,method,*args)

def rpcServer(port=1212,ip='0.0.0.0',currentThread=False):
	if py.is3():
		from xmlrpc.server import SimpleXMLRPCServer as RPCServer
	U=py.importU()
	with RPCServer((ip, port),allow_none=True,use_builtin_types=True ) as server:
		server.register_function(eval)
		server.register_function(U.execResult, 'execute')
		server.register_instance(U, allow_dotted_names=True)
		if currentThread:
			server.serve_forever()
		else:
			from threading import Thread
			t=Thread(target=server.serve_forever)
			t.start()
			return t

def rpcClient(url_or_port='http://127.0.0.1:1212'):
	if py.isint(url_or_port):
		url='http://127.0.0.1:'+str(url_or_port)
	else:
		url=str(url_or_port)
	
	if py.is3():
		from xmlrpc.client import ServerProxy,MultiCall
	server = ServerProxy(url)
	return server
	
def get_ip_from_mac(mac):
	'''mac=='' return all ip
	'''
	U=py.importU()
	T=U.T
	r=U.cmd('arp','-a').splitlines() 
	r=[T.sub(i,'  ', '   ') for i in r if mac in i]
	r=[i for i in r if i]
	if py.len(r)==0:
		return py.No('no ip match mac:{} in arp table!'.format(mac))
	if py.len(r)>1:
		return py.No('more then 1 ip matched mac:{} in arp table!'.format(mac),r)
	if py.len(r)==1:
		return r[0]

def getLAN_IP():
	r=getAllAdapter()
	return r

def getAllAdapter():
	U=py.importU()
	if U.iswin():
		from qgb import Win
		return Win.getAllNetworkInterfaces()
	
#setip 192.168  ,  2.2	
def setIP(ip='',adapter='',gateway='',source='dhcp',mask='',ip2=192.168):
	if not adapter:
		#adapter=u'"\u672c\u5730\u8fde\u63a5"'.encode('gb2312')#本地连接
		try:
			adapter=getAllAdapter()[0][0]	#   ( [11,'192.168.1.111',..] , [..] , ..]
		except:	
			if py.is2():adapter="\xb1\xbe\xb5\xd8\xc1\xac\xbd\xd3"
			else:		adapter="本地连接"
		# from qgb import Win
		# if Win.isxp():
			
	if ip:
		source='static'
		if type(ip) is py.int:
			ip='{0}.2.{1}'.format(ip2,ip)
		if type(ip) is py.float:
			ip='{0}.{1}'.format(ip2,ip)
		# if not ip.startswith('addr='):ip='addr='+ip
		if not mask:mask='255.255.255.0'
		# if not mask.startswith('mask'):mask='mask='+mask
		if not gateway:
			T=py.importT()
			gateway=T.subLast(ip,'','.')+'.1'
	else:
		ip=''
	r='netsh interface ip  set address name={0} source={1} address={2} mask={3} gateway={4} '.format(adapter,source,ip,mask,gateway)
	import os
	os.system(r)
	return r
setip=setIP
def getComputerName():
	import socket
	return socket.gethostname()
gethostname=getHostName=getComputerName

def getArpTable():
	U=py.importU()
	return U.cmd('arp -a')
		
def scanPorts(host,threadsMax=33,from_port=1,to_port=65535,callback=None,ip2=192.168):
	'''return [opens,closes,errors]
	callback(*scanReturns)
	if callback and ports> threadsMax: 剩下结果将异步执行完成
	'''
	py.importU()
	from threading import Thread
	import socket
	# host = raw_input('host > ')
	# from_port = input('start scan from port > ')
	# to_port = input('finish scan to port > ')   
	counting_open = []
	counting_close = []
	errors=[]
	threads = []
	if isinstance(host,py.float):host='{0}.{1}'.format(ip2,host)
	
	def scan(port):
		# U.count(1)
		try:
			s = socket.socket()
			result = s.connect_ex((host,port))
			# U.pln('working on port > '+(str(port)))      
			if result == 0:
				counting_open.append(port)
				#U.pln((str(port))+' -> open') 
				s.close()
			else:
				counting_close.append(port)
				#U.pln((str(port))+' -> close') 
				s.close()
		except Exception as e:
			errors.append({port:e})
	def newThread(port):
		t = Thread(target=scan, args=(i,))		
		threads.append(t)
		try:
			t.start()
		except:
			"can't start new thread"
	im=py.float(to_port-from_port+1)
	percent=0.0
	for i in range(from_port, to_port+1):
		if (i/im>percent):
			U.pln( 'Scanning  %.0f%%' % (percent*100), len(threads)     )
			percent+=0.01
			
		if len(threads)<=threadsMax:
			newThread(i)
		else:
			for x in threads:
				if x.isAlive():
					x.join()
					newThread(i)
				else:
					threads.remove(x)
				break
	# if callback:
		# return callback
	[x.join() for x in threads]
	return [counting_open,counting_close,errors]
	

if __name__=='__main__':
	U.pln( getLAN_IP())
	exit()
	gsurlip=['http://ip.chinaz.com/getip.aspx'][0]
	
	
	s=http(gsurlip)#.encode('utf8').decode('mbcs')
		 
		 
	U.pln( s.decode('utf8').encode('mbcs'))
	# import chardet
	# U.pln( chardet.detect(s)
	
