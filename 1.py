#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author@Haris Wang
import requests
import json

header = {"User-Agent": "Mozilla/5.0 (Linux; Android 10;  AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045136 Mobile Safari/537.36 wxwork/3.0.16 MicroMessenger/7.0.1 NetType/WIFI Language/zh",
}

libUrl = [
  "http://lib.scu.edu.cn:8088/reservation_myaccount/%E5%B7%A5%E5%AD%A6%E9%A6%86", #工学馆
  "http://lib.scu.edu.cn:8088/reservation_myaccount/%E6%B1%9F%E5%AE%89%E9%A6%86", #江安馆
  "http://lib.scu.edu.cn:8088/reservation_myaccount/%E6%96%87%E7%90%86%E9%A6%86", #文理馆
  "http://lib.scu.edu.cn:8088/reservation_myaccount/%E5%8C%BB%E5%AD%A6%E9%A6%86"  #医学馆

]

def makeLibResv(stu_id, passwd):
        login_data = {
                "form_id" : "studentlogin",
                "academic" : stu_id,
                "passwd" : passwd,
                "op" : "登录"
        }

        s = requests.Session()
        s.headers.update(header)
        ret = s.post("http://lib.scu.edu.cn:8088/student/login?from=reservation", data=login_data)
        ret = s.get("http://lib.scu.edu.cn:8088/reservation")
        if "江安馆" not in ret.text:
                print("login in - FAILED!!!!")
                return 0
        if "您已预约" in ret.text:
                print("Already Reserved !!!!")
                return 0
        ret = s.get(libUrl[1])
        ret = s.get("http://lib.scu.edu.cn:8088/reservation")
        if "您已预约" not in ret.text:
                print("Reservation - FAILED!!!!")
                return 0
        return 1

data = []
with open("login.json", "r") as f:
        data = json.load(f)

for item in data:
        rc = makeLibResv(item["u"], item["p"])
        if rc:
            print("{} 本次预约成功！！！".format(item["u"]))
        else:
            print("{} 本次预约失败！！！".format(item["u"]))
