#coding=utf-8
#返回值需要使用更新全局变量函数。返回值全局变量为 LASTRET
from . import graphic

def consoleOut(identity,_content,leftColor='grey',rightColor='grey',colorStr='n0p'):
    #向N0Shell控制台输出的标准函数
    pass
def debugOut(identity,_content,leftColor='grey',rightColor='grey',colorStr='n0p'):
    #在Debug模式下才会输出
    pass
def argv(id):
    #获取N0Shell参数
    pass
def newArgv(offset):
    pass
def realPath(_path,isFile=False):
    #将文件名或目录转为可访问路径
    pass
def openFile(fileName):
    #打开文件 返回一个文件对象
    pass
def request(_method,targetURL,paramsData,postData,_header):
    #发送请求 get post json paramsData postData _header均为dict类型
    pass
def urlSpliter(targetUrl):
    #切分url 返回多个参数 protocol,domain,port,urlPath,fileName
    pass
def publicVar(publicVarName):
    #访问全局变量
    pass
def publicVarSync(publicVarName,_data):
    #更新全局变量
    pass