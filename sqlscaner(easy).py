#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from fake_useragent import UserAgent

ua = UserAgent()
s = requests.Session()
s.headers["User-Agent"] = ua.random

def get_all_froms(url):
    soup = BeautifulSoup(s.get(url).content,'lxml')
    return soup.find_all("form")

#详细的解析
#这个函数用来提取关于html表单所有的有用信息
def get_form_details(form):
    details = {}
    #获取表单的action
    try:
        action = form.attrs.get("action").lower()
    except:
        action = None
    #获取表单的方法（get post）
    method = form.attrs.get("method","get").lower()
    #获取一些输入的细节，比如类型，名称
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type","text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value")
        inputs.append({"type":input_type,"name":input_name,"value":input_value})
    
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

#判断是否存在sql注入
def is_vulnerable(response):
    errors = {
        #mysql
        "you have an error in your sql syntax;",
        "warning:mysql",
        #sqlserver
        "unclosed quotation mark after the charcter string",
        #Oracle
        "qupted string not properly terminated",
    }
    for error in errors:
        # print(error)
        if error in response.content.decode().lower():
            return True
    return False
        
def scan_sql_injection(url):
    #测试url
    for c in "\"'":
        new_url = f"{url}{c}"
        print("正在尝试",new_url)
        res = s.get(new_url)
        # print(res.content)
        # print(is_vulnerable(res))
        if is_vulnerable(res):
            print("找到sql注入漏洞 链接：",new_url)
            return
        
    #测试表单
    forms = get_all_froms(url)
    for form in forms:
        form_details = get_form_details(form)
        for c in "\"'":
            #提交测试的数据体
            data = {}
            for input_tag in form_details["inputs"]:
                #测试任何隐藏的或者有值的输入
                if input_tag["type"] == "hidden" or input_tag["value"]:
                    #只需要在表单的主体中使用他
                    try:
                        data[input_tag["name"]] = input_tag["value"] + c
                    except:
                        pass
                elif input_tag["type"] != "submit":
                    #其余的标签全都用上带有测试的字符
                    data[input_tag["name"]] = f"test{c}"
        #url拼接起来
        url = urljoin(url,form_details["action"])
        if form_details["method"] == "post":
            res = s.post(url,data=data)
        elif form_details["method"] == "get":
            res = s.get(url,params=data)
        if is_vulnerable(res):
            print("SQL注入漏洞存在 链接：",url)
            print("Form:")
            print(form_details)
            break
        
if __name__ == '__main__':
    url = "http://testphp.vulnweb.com/artists.php?artist=1"
    scan_sql_injection(url)                             
                    
                              