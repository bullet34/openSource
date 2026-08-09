import asyncio

async def client():
    reader, writer = await asyncio.open_connection(
        "127.0.0.1",
        5000
    )

    print("서버에 연결됨")

    # 서버로 요청 보내기
    message = "hello"
    writer.write(message.encode())
    await writer.drain()

    # 서버 응답 기다리기
    data = await reader.read(1024)

    if data:
        print("서버에서 받은 데이터:", data.decode())

    writer.close()
    await writer.wait_closed()


asyncio.run(client())
