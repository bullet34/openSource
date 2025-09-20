import time
import asyncio


async def start1(): # 비동기함수
    for i in range(1, 11):
        print(i)
        await asyncio.sleep(1)

def start2():   # 동기함수
    for i in range(5, 0, -1):
        print("%s 입니다" % i)
        time.sleep(1)

async def new():
    task = asyncio.create_task(start1())   # (함수(인자)) 비동기 함수를 메인스레드에서 실행, 바로 실행    
    await asyncio.to_thread(start2) # (함수, 인자)  동기함수를 별도의 스레드에서 등록하고 비동기적으로 실행함, 실행은 await 구문에서 실행됨
    
    task.cancel()  # 실행 취소
    
    # task 객체가 완료될 때까지 기다리거나 취소로 인한 예외처리
    try:
        await task
    except:
        pass
    print("task 취소")


def main():
    asyncio.run(new())  # 프로그램 최상위에서 비동기함수 실행
    
    
if __name__ == '__main__':
    main()
    
