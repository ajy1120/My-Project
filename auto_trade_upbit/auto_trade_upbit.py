from pyupbit import Upbit
import time

#Open API를 통해 키를 발급받아 본인이 입력하게 해야함.
#Access Key 외 Secret Key 가 틀리면 틀렸다고 출력되게 해야되고, 겹쳐서 다른 사람의 키로 로그인 되었을 경우 존재하는가?

class Upbit_Trade:
    def __init__(self,access,secret):
        self.access=access
        self.secret=secret

    def auto_trade(self,current_price): #access key, secret key 를 받아서 로그인. 
        info=Upbit(self.access,self.secret) #Upbit 객체 생성.    
    
        print("Start\n")

        while True:
            try:
                if current_price>5000: #current_price 는 딱히 비교할게 없어 그냥 적어놓은 변수임.
                    myaccount=info.get_balance("KRW") #잔고 조회
                    print("sell market order") 
                    info.sell_market_order("KRW-BTC",myaccount*0.95) # 비트코인 시장가 매도
                    if myaccount==0:
                        print("account 0")
                        break
                
                else:
                    myaccount=info.get_balance("KRW")
                    print("buy market order")
                    info.buy_market_order("KRW-BTC",myaccount*0.95) # 비트코인 시장가 매수
                    if myaccount==0:
                        print("account 0")
                        break
            
            except Exception as e:
                print(e)
                time.sleep(1)
            

     
    def krw_price_check(self): #파이썬에서 메서드를 호출할 때 메서드가 있는 객체 자신이 인자로 들어가기 때문.
         upb=Upbit(self.access,self.secret)
         
         all_coin=upb.get_tickers("KRW")

         for i in all_coin:
             a=upb.get_current_price(i) # 현재가 조회
             print(i,":",a," KRW")
             time.sleep(0.03) # 업비트 API 호출 제한. 
# 의미없는 메소드. 가격은 계속 바뀌는데 불러오는 속도 넘 느림..
    

if __name__ == "__main__":
    print("Access 키와 Secret 키를 입력해야 합니다.") # 직접 입력
    print("Access Key : ")
    ac=input()
    print("Secret Key : ")
    sec=input()

    up=Upbit_Trade()
    up.auto_trade(ac,sec)

#   with open("key.txt") as f:   # 메모장에 키를 입력하고 그것을 받아오는 방법    
#        lines=f.readlines()
#        access=lines[0].strip()
#        secret=lines[1].strip()
    
    y=Upbit_Trade()
    #y.auto_trade()

