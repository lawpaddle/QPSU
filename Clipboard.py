#coding=utf-8
try:from . import py
except:import py
# 因为 Clipboard 在 qgb.U 中 较早加载，此时又引入其他模块 容易造成循环引用 引起 其他问题。
try:
	import win32clipboard as w
	import win32con
except Exception as err:
	gError=err

def get(p=0):
	'''win32con.
CF_DSPTEXT     ', 129],
CF_OEMTEXT     ', 7],
CF_RETEXTOBJ   ', 'RichEdit Text and Objects'],
CF_TEXT        ', 1],
CF_UNICODETEXT ', 13],
	
	in py3 win32con.CF_TEXT return b' '
	'''
	U=py.importU()
	if U.istermux():return U.cmd('termux-clipboard-get') 
	
	w.OpenClipboard()
	d = w.GetClipboardData(win32con.CF_UNICODETEXT)
	w.CloseClipboard()
	if p:U.pln(d)
	return d

def set(aString,p=0):
	U=py.importU()
	if p:print(py.repr(aString))
	if U.istermux():return U.cmd('termux-clipboard-set',input=aString) 
	try:
		w.OpenClipboard()
		w.EmptyClipboard()
		# w.SetClipboardData(win32con.CF_TEXT, aString)
		w.SetClipboardText(aString)
	finally:
		w.CloseClipboard()

def set_repr(a):
	return set(repr(a))
setr=setRepr=set_repr

def close():
	w.CloseClipboard()


def get_image(file=None,format='png'):
	''' :param fp: A filename (string), pathlib.Path object or file object.

KeyError: '.PNG'  [format not contains . ]
	'''
	global gsdir
	U,T,N,F=py.importUTNF()
	from PIL import ImageGrab,Image
	im = ImageGrab.grabclipboard()
	if im and file:
		# if not im:
			# return 
		if not F.isAbs(file):
			gsdir=F.md(U.gst+'clipboard')
			file=gsdir+file
		if not file.lower().endswith(format.lower()):
			file=file+'.'+format
		im.save(file,format)
		return file
	if not im:
		return py.No('can not get clipboard image')
	return im
get_img=get_image
###############################	
def getTypeList():
	'''cb.set('===============')
	for i in range(1,65536):
[[1, b'==============='],
 [7, b'==============='],
 [13, '==============='],
 [16, b'\x04\x08\x00\x00']]
 
 other:if d.args==('Specified clipboard format is not available',):continue
 TypeError('Specified clipboard format is not available')
 '''
	w.OpenClipboard()
	r={}
	i=0
	while True:
		i=w.EnumClipboardFormats(i)
		if not i:break
		try:
			d=w.GetClipboardData(i)
		except Exception as e:
			r[i]=e
		else:	
			r[i]=d
			# r.append([i,d])
	w.CloseClipboard()# 未close 会导致 clipboard 无法使用
	return r

#set(get()[0:5])	


#import T



#import U
#U.test()
