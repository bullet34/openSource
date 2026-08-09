import asyncio

async def server():
    server = await asyncio.start_server(  # TCP socket 통신서버 생성
        handle_client,
        "127.0.0.1",  # ip
        5000  # 포트
    )

    async with server:
        await server.serve_forever()  # 서버생성후 클라이언트로부터 연결 대기 지속 


async def handle_client(reader, writer):

    while True:
        data = await reader.read(1024) # 클라이언트의 데이터를 계속 읽음 (1024바이트)

        if not data:  # 클라이언트가 연결을 ''반환
            break

        print("받은 데이터:", data)  # 받은 데이터 확인

        writer.write(data)  # 받은 데이터를 그대로 클라이언트로 전송

        await writer.drain()   # 전송이 끝날 때까지 기다림

    # 연결 종료
    writer.close()
    await writer.wait_closed()  # 종료완료까지 대기

asyncio.run(server())
