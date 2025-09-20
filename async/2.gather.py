import time
import asyncio


def start1():   # 동기함수
    for i in range(1, 11):
        print(i)
        time.sleep(1)

def start2():   # 동기함수
    for i in range(5, 0, -1):
        print("%s 입니다" % i)
        time.sleep(1)

async def new():
    
    a = asyncio.to_thread(start1)  # 별도의 스레드 및 코루틴 객체 생성
    b = asyncio.to_thread(start2)
    
    await asyncio.gather(a, b) # await 시점에서 a, b 코루틴 객체 실행, gather함수 - a와 b코루틴을 동시에 실행하도록 스케쥴링
    
    print("완료!")


def main():
    asyncio.run(new())  # 프로그램 최상위에서 비동기함수 실행
    
    
if __name__ == '__main__':
    main()
