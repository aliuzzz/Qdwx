from calendar import month
import os
import re
import os.path #文件夹遍历函数  
from time import sleep
import datetime
import logging
import sys

#now_time = datetime.datetime.now()
#year =str(now_time.strftime('%Y'))
#month1 =str(now_time.strftime('%m'))
#day =str(now_time.strftime('%d'))

#拼接
def pinjie():
    filedir = 'D:/Users/Worker/Desktop/yuliao/测试'#获取目标文件夹的路径
    #filedir = '/data/mtr/'+year+'年'+month1+'月/'+year+'年'+month1+'月'+day+'日/测试'
    filenames=os.listdir(filedir)#获取当前文件夹中的文件名称列表
#打开当前目录下的result.txt文件，如果没有则创建
    dirs = 'D:/Users/Worker/Desktop/yuliao/jieguo'
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    sleep(1)
    f=open('D:/Users/Worker/Desktop/yuliao/jieguo/result.txt','w')
#先遍历文件名
    for filename in filenames:
        filepath = filedir+'/'+filename
        #遍历单个文件，读取行数
        for line in open(filepath):
            f.writelines(line)
        f.write('\n')
    #关闭文件
    f.close()
    sleep(2)
    logging.basicConfig(
        filename='D:/Users/Worker/Desktop/yuliao/log/a.log',
        level=logging.DEBUG,
        format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]'
    )
    logging.debug('拼接完成')

def tongji(file_path):
    global count
    log = open(file_path, 'r')
    C = r'\.'.join([r'\d{1,3}']*4)
    find = re.compile(C)
    count={}
    for i in log:
        for ip in find.findall(i):
            count[ip] = count.get(ip,1) + 1
    
def jisuan():
    num = 0
    R=count.items()
    with open('D:/Users/Worker/Desktop/yuliao/jieguo/result2.txt','a') as file0:
        for i in R:
            if i[1] > 0:
                print(i,file=file0)
                num+=1
        print('----------------------------',file=file0)
    logging.basicConfig(
        filename='D:/Users/Worker/Desktop/yuliao/log/a.log',
        level=logging.DEBUG,
        format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]'
    )
    #print('符合数量: %s'%(num))
    logging.debug('符合数量: %s'%(num))

if __name__ == '__main__':
    pinjie()
    #num = 0
    tongji(r'D:/Users/Worker/Desktop/yuliao/jieguo/result.txt')
    jisuan()
    '''
    R=count.items()
    with open('D:/Users/Worker/Desktop/yuliao/jieguo/result2.txt','a') as file0:
        for i in R:
            if i[1] > 0:
                print(i,file=file0)
                num+=1
    print('符合数量: %s'%(num))
    '''