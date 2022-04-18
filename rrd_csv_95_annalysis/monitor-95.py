import requests
import datetime
import time
from selenium import webdriver
import requests
import pandas as pd
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless') 
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--window-size=1920,1080')
driver = webdriver.Chrome(options=chrome_options)
driver.get(cacti网址)
#driver.implicitly_wait(5)
user = 用户名
passwd = 密码

#登录并且下载csv表格和图片
def selenium_login():
    #----------selenium登录------------------------------------------------
    zhanghu = driver.find_element(By.CSS_SELECTOR, '[name="login_username"]')
    mima = driver.find_element(By.CSS_SELECTOR, '[name="login_password"]')
    zhanghu.send_keys(user)
    mima.send_keys(passwd)
    driver.find_element(By.CSS_SELECTOR,'[value="Login"]').click()
    driver.find_element(By.CSS_SELECTOR,'[alt="Graphs"]').click()
    cookie = driver.get_cookies()
    print(cookie)
    print(type(cookie))
    cookie_str =''
    for cook in cookie:
        cookie_str +=cook.get('name')+'='+ cook.get('value')
               # if cook.get('name') == 'Cacti':
     #         cookie_str = cook.get('value')
    print(cookie_str)    
   
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        'content-type': 'text/html; charset=UTF-8',
        'Referer': 登陆后ip
    }
    cookie_data = {
      'Cookie':'完整的cookie=cookie+cookie_str+''; _gat=1'
    }
    
    #-------------------------处理日期------------------------------------------

    # 当天的日期
    today_date = datetime.datetime.now().date()
    # 当月1号
    one_date = datetime.datetime.now().replace(day=1)
    # 当天的零点
    today_zero_time = get_day_zero_time(today_date)
    # 当月1号零点
    one_zero_time = get_day_zero_time(one_date)

    #------------------------------------------------------------------------

    #--------------------------下载csv文件------------------------------------
    # 建立一个字典存储要下载的csv对应的地区id
    num_list = {'id':'name'
    }
    
    # 用带cookie的方法下载,下载的为当月1号0点到当天0点的csv
    for num,value in num_list.items():
        Downloadcsv_address = 'http://ip/cacti/graph_xport.php?local_graph_id=' + num + '&rra_id=0' \
                              '&view_type=tree&graph_start=' + str(one_zero_time) + '&graph_end=' + str(today_zero_time)
        print(Downloadcsv_address)
        file_address = "存放路径" + value + ".csv"  # 存放路径
        r = requests.get(Downloadcsv_address, headers=headers, cookies=cookie_data)
        with open(file_address, "wb") as code:
            code.write(r.content)
        print(num, 'Download success!')

    driver.quit()
    #------------------------------------------------------------------------

#获取0：00的时间戳
def get_day_zero_time(date):
    if not date:
        return 0

    date_zero = datetime.datetime.now().replace(year=date.year, month=date.month,

    day=date.day, hour=0, minute=0, second=0)

    date_zero_time = int(time.mktime(date_zero.timetuple()))

    return(date_zero_time)

#处理表格形成结果
def csv_deal():
    # 新建一个result.txt文件------------------------------------------------
    with open("result.txt",'w+',encoding='utf-8') as f:
            #打印当前文件名
        print('当前时间：',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),file=f)
        print('\n',file=f)
    #------------------------------------------------------------------------
    
    #读文件-------------------------------------------------------------------
    Directory_name = r'文件路径'
    filenames = os.listdir(Directory_name)
    print("读取到以下文件：",filenames)
    for csvname in filenames:
        filename = (Directory_name+"/"+csvname)
        print(filename)
    #------------------------------------------------------------------------

    #-----------处理表格-----------------------------------------------------
        # 找到第一个空行位置
        blank_line = 0
        with open(filename,'r',encoding='utf8') as f:
            for (num,value) in enumerate(f):
                if num == 8:
                    print(filename,'表显95值为:')
                    print(value.split(',',2)[1])#打印在表格里显示的图中的95详细值
                    no_95 = value.split(',',2)[1]
                if value.strip() == '""':
                    blank_line = num + 1
                    break

        # 读文件，跳过无效头部
        df = pd.read_csv(filename, skiprows=blank_line)

        # 删除第一列
        df.drop(df.columns[0], inplace=True, axis=1)

        # 删除匹配 "col" 的列
        df.drop(list(df.filter(regex='col')), axis=1, inplace=True)

        # 主从降序排输入值列
        p_col = ['inbound', 'outbound']
        df.columns = p_col
        df.sort_values(by=['inbound', 'outbound'], ascending=False, inplace=True)

    #------------------------------------------------------------------------
        
    #-----------处理数据-----------------------------------------------------    
        print("输入相关信息：")
        #取总行数的0.05做为95值的位置
        no_one = round(len(df)*0.05)
        no_two = round(len(df)*0.05)+1
        no_three = round(len(df)*0.05)+2
        no_one_x = no_one+1
        no_two_y = no_two+1
        no_three_z = no_three+1
        
        #定位95值的具体数字
        no_one_value = float(df.iloc[[no_one],[0]].values)
        no_two_value = float(df.iloc[[no_two],[0]].values)
        no_three_value = float(df.iloc[[no_three],[0]].values)

        show_one = str(no_one_x)+"值为："+str(no_one_value)+"字节"
        show_two = str(no_two_y)+"值为："+str(no_two_value)+"字节"
        show_three = str(no_three_z)+"值为："+str(no_three_value)+"字节"

        no_443 = df.iloc[442]['inbound']/1000/1000/1000
        #保留两位小数
        no_443 = round(no_443,2)
        no_443_in=str(no_443)+"GB\n"

        with open("result.txt",'a+',encoding='utf-8') as f:
            print('---------------------Inbound----------------\n',file=f)
            print('表中95值位置：',str(no_95),file=f)
            print('** 443值为：',no_443_in,file=f)
            print(filename,file=f)
            print(show_one,file=f)
            print(show_two,file=f)
            print(show_three,file=f)
            print('\n',file=f)
        time.sleep(1)

        #更改顺序，主从降序排输出值列
        df.sort_values(by=['outbound', 'inbound'], ascending=False, inplace=True)

        print("输出相关信息：")
        no_one_value = float(df.iloc[[no_one],[1]].values)
        no_two_value = float(df.iloc[[no_two],[1]].values)
        no_three_value = float(df.iloc[[no_three],[1]].values)

        show_one = str(no_one_x)+"值为："+str(no_one_value)+"字节"
        show_two = str(no_two_y)+"值为："+str(no_two_value)+"字节"
        show_three = str(no_three_z)+"值为："+str(no_three_value)+"字节"   

        no_443 = df.iloc[442]['outbound']/1000/1000/1000
        #保留两位小数
        no_443 = round(no_443,2)
        no_443_out=str(no_443)+"GB\n"

        with open("result.txt",'a+',encoding='utf-8') as f:
            print('---------------------Outbound----------------',file=f)
            print('表中95值位置：',str(no_95),file=f)
            print('***443值为：',no_443_out,file=f)
            print(filename,file=f)
            print(show_one,file=f)
            print(show_two,file=f)
            print(show_three,file=f)
            print('\n',file=f)
        #----------------------------------------------------------------
        #  Save as
        #df.to_csv('new1.csv', index=False, encoding='utf-8')
        df.to_csv('文件路径'+csvname, index=False, encoding='utf-8')




if __name__ == '__main__':
    selenium_login()
    csv_deal()