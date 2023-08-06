
def proxies(welcome_to_my_world):
    import os
    os.system('pip install requests')
    import json
    import requests
    from threading import Thread
    import sys
    limit = int(float(input('num of proxies >> ')))
    proxy = requests.get('http://pubproxy.com/api/proxy?api=')
    f = open("proxies.txt","w+")
    def putData(p, t, l, x = 1):
        data = p.text
        data = json.loads(data)
        data = json.dumps(data['data'][0])
        data = json.loads(data)
        f= open("result_proxies.kemo.txt","a+")
        f.write(data['ipPort']+'\n')
        print(x, end='\r')
        d = requests.get('http://pubproxy.com/api/proxy?type='+t+'&api=')
        if x == l:
            print('Finishid !! saved as result_proxies.kemo.txt')
        else:
            xx = x + 1
            putData(d, t, l, xx)
    def start(limit, proxy):
        print('[1] : Http \n[2] : socks4\n[3] : socks5')
        ty = input('type of proxy >> ')
        if ty == '1':
            print('okay \nNow we are creating proxy for you please wait')
            thread = Thread(target = putData, args = (proxy, 'http', limit))
            thread.start()
        elif ty == '2':
            thread = Thread(target = putData, args = (proxy, 'socks4', limit))
            thread.start()
        elif ty == '3':
            thread = Thread(target = putData, args = (proxy, 'socks5', limit))
            thread.start()
        else:
            sys.exit('worn number\nread again please')
    thread = Thread(target = start, args = (limit, proxy))
    thread.start()

def searcher(welcome_to_my_world):
    from threading import Thread    
    def search():
        import time
        import os
        print("Installing module wait....")
        time.sleep(2)
        os.system('pip install google')
        from googlesearch import search 
        print(' \r\n')
        s = input("search >> ")
        d = input("number of links >> ")
        for j in search(s, tld="co.in", num=int(d), stop=int(d), pause=2): 
            print(j)
            f= open("result_search.kemo.txt","a+")
            f.write(str(j)+'\n')
            print('finish!! save as result_search.kemo.txt', end='\r')
    
    def check():
        import time
        import os
        print("Installing module wait....")
        time.sleep(2)
        os.system('pip install requests')
        from threading import Thread
        import sys
        import os
        import time
        print('Show text file  wait...')
        time.sleep(2)
        for file in os.listdir():
            if file.endswith(".txt"):
                print(os.path.join(file))

        files = input('enter host file >> ')
        mfile = open(files, "r+")
        lines = mfile.readlines()
        line = len(lines)
        def response(li, l, x = 0):
            print(x+1, end='\r')
            import requests
            host = li[x]
            host = host.replace('https://', '')
            host = host.replace('http://', '')
            host = host.replace('\n', '')
            host = 'http://'+host
            try:
                r = requests.get(host, timeout=(1, 5))
                code = r.status_code
                f= open("result.txt","a+")
                f.write(host+'          '+str(code)+'\n')
            except requests.ConnectionError:
                f= open("result.txt","a+")
                f.write(host+'          '+'not vaild'+'\n')
            if x != l-1:
                xx = x + 1
                response(li, l, xx)
            else:
                print('Finish!! saved as result.txt')
                sys.exit()
        thread = Thread(target = response, args = (lines, line))
        thread.start()
    def starts():
        print('welcome kemo searcher!!\n[1] : search + get urls     (dorks, words, ...)\n[2] : check urls     (vaild, unvaild, status_code)')
        s = input('Your choice >> ')
        if s == '1':
            search()
        elif s == '2':
            check()
        else:
            print('wrong choice')
    thread = Thread(target = starts)
    thread.start()

