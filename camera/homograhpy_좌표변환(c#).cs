using System;
using OpenCvSharp;

class Program
{
    static void Main()
    {
        // 이미지상의 점
        Point2f[] imagePoints =
        {
            new Point2f(120, 80),
            new Point2f(520, 100),
            new Point2f(560, 450),
            new Point2f(80, 420),
            new Point2f(300, 200),
            new Point2f(400, 250),
            new Point2f(200, 300),
            new Point2f(450, 350),
            new Point2f(250, 400),
            new Point2f(350, 450)
        };

        // 각 점에 대응하는 실제 좌표
        Point2f[] worldPoints =
        {
            new Point2f(0.0f, 0.0f),
            new Point2f(4.0f, 0.0f),
            new Point2f(4.0f, 6.0f),
            new Point2f(0.0f, 6.0f),
            new Point2f(1.5f, 2.0f),
            new Point2f(2.7f, 2.5f),
            new Point2f(1.0f, 3.0f),
            new Point2f(3.2f, 4.0f),
            new Point2f(1.8f, 4.5f),
            new Point2f(2.8f, 5.2f)
        };

        // Homography 계산
        using Mat imageMat = InputArray.Create(imagePoints).GetMat();
        using Mat worldMat = InputArray.Create(worldPoints).GetMat();

        using Mat mask = new Mat();

        Mat H = Cv2.FindHomography(
            imageMat,
            worldMat,
            HomographyMethods.Ransac,
            3.0,
            mask
        );

        Console.WriteLine("Homography Matrix:");
        Console.WriteLine(H);

        // -----------------------------
        // 좌표 변환
        // -----------------------------

        Point2f point = new Point2f(350, 300);

        Point2f[] inputPoint =
        {
            point
        };

        Point2f[] worldPoint = Cv2.PerspectiveTransform(
            inputPoint,
            H
        );

        Console.WriteLine();
        Console.WriteLine("Image Point:");
        Console.WriteLine($"X = {point.X}, Y = {point.Y}");

        Console.WriteLine();
        Console.WriteLine("World Point:");
        Console.WriteLine($"X = {worldPoint[0].X}, Y = {worldPoint[0].Y}");

        H.Dispose();
    }
}
