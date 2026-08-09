using System;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

class Program
{
    static async Task Client()
    {
        using TcpClient client = new TcpClient();

        // 서버 연결
        await client.ConnectAsync("127.0.0.1", 5000);

        Console.WriteLine("서버에 연결됨");

        using NetworkStream stream = client.GetStream();

        // 서버로 요청 보내기
        string message = "hello";
        byte[] sendData = Encoding.UTF8.GetBytes(message);

        await stream.WriteAsync(sendData, 0, sendData.Length);

        // 서버 응답 기다리기
        byte[] buffer = new byte[1024];

        int bytesRead = await stream.ReadAsync(
            buffer,
            0,
            buffer.Length
        );

        if (bytesRead > 0)
        {
            string response = Encoding.UTF8.GetString(
                buffer,
                0,
                bytesRead
            );

            Console.WriteLine("서버에서 받은 데이터: " + response);
        }
    }

    static async Task Main()
    {
        await Client();
    }
}
```
