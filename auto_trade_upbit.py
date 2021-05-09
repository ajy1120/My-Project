import pyupbit
import time

#Open API를 통해 키를 발급받아 0본인이 입력하게 해야함.
#Access Key 외 Secret Key 가 틀리면 틀렸다고 출력되게 해야되고, 겹쳐서 다른 사람의 키로 로그인 되었을 경우 존재하는가?

class Upbit_Trade:
    def __init__(self): 
        

    def auto_trade(self,access,secret,current_price): #access key, secret key 를 받아서 로그인.
        info=Upbit(access,secert) #Upbit 객체 생성.

        if info == -1:
            print("Login False")
        
        while True:
            print("Auto-Trade Start\n")
            
            if current_price>5000:
                info.sell_market_order()
            else:
                info.buy_market_order()
                
    # def krw_price_check(self): #파이썬에서 메서드를 호출할 때 메서드가 있는 객체 자신이 인자로 들어가기 때문.
    #     all_coin=pyupbit.get_tickers("KRW")

    #     for i in all_coin:
    #         a=pyupbit.get_current_price(i) # 현재가 조회
    #         print(i,":",a," KRW")
    #         time.sleep(0.03) # 업비트 API 호출 제한 때문에 넣음.

    

if __name__ == "__main__":
#    print("Access 키와 Secret 키를 입력해야 합니다.") # 직접 입력
#    print("Access Key : ")
#    ac=input()
#    print("Secret Key : ")
#    sec=input()

#    login=input_info(ac,sec)

#   with open("key.txt") as f:      
#        lines=f.readlines()
#        access=lines[0].strip()
#        secret=lines[1].strip()
    
    y=Upbit_Trade()
    y.krw_price_check()

