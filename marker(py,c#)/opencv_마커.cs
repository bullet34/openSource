using System;
using System.Collections.Generic;
using OpenCvSharp;

class Program
{
    // 마커 좌표 저장
    static List<Point> markers = new List<Point>();

    static Mat img;

    static void MouseCallback(
        MouseEvent @event,
        int x,
        int y,
        MouseEventFlags flags,
        IntPtr userdata)
    {
        if (@event == MouseEvent.LButtonDown)
        {
            markers.Add(new Point(x, y));

            Console.WriteLine($"마커 추가: ({x}, {y})");
        }
    }

    static void DrawMarkers(Mat frame)
    {
        for (int i = 0; i < markers.Count; i++)
        {
            Point p = markers[i];

            int x = p.X;
            int y = p.Y;

            // 사각형
            Cv2.Rectangle(
                frame,
                new Point(x - 20, y - 20),
                new Point(x + 20, y + 20),
                new Scalar(255, 0, 0),
                2
            );

            // 원형 마커
            Cv2.Circle(
                frame,
                p,
                8,
                new Scalar(0, 0, 255),
                -1
            );

            // 십자 표시
            Cv2.DrawMarker(
                frame,
                p,
                new Scalar(0, 255, 0),
                MarkerTypes.Cross,
                20,
                2
            );

            // 마커 번호 + 좌표
            Cv2.PutText(
                frame,
                $"M{i + 1} ({x}, {y})",
                new Point(x + 15, y - 15),
                HersheyFonts.HersheySimplex,
                0.5,
                new Scalar(255, 255, 255),
                1
            );
        }
    }

    static void Main()
    {
        // 이미지 불러오기
        img = Cv2.ImRead(
            "picture_calib/camera2_21.jpg"
        );

        // 이미지 로드 확인
        if (img.Empty())
        {
            Console.WriteLine("이미지를 불러오지 못했습니다.");
            return;
        }

        // 윈도우 생성
        Cv2.NamedWindow("Camera");

        // 마우스 콜백 등록
        Cv2.SetMouseCallback(
            "Camera",
            MouseCallback
        );

        while (true)
        {
            // 원본 이미지 복사
            using Mat frame = img.Clone();

            // 마커 표시
            DrawMarkers(frame);

            // 화면 출력
            Cv2.ImShow("Camera", frame);

            // 키 입력
            int key = Cv2.WaitKey(30);

            // ESC -> 종료
            if (key == 27)
            {
                break;
            }

            // R -> 마커 전체 삭제
            else if (key == 'r' || key == 'R')
            {
                markers.Clear();

                Console.WriteLine("마커 삭제");
            }
        }

        Cv2.DestroyAllWindows();
        img.Dispose();
    }
}
