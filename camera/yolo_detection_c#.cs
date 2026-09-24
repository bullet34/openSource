//using Microsoft.ML.OnnxRuntime;
//using Microsoft.ML.OnnxRuntime.Tensors;
//using OpenCvSharp;
//using OpenCvSharp.Dnn;
//using System;
//using System.Collections.Generic;
//using System.Drawing;
//using System.Linq;

//class Program
//{
//    static void Main(string[] args)
//    {
//        string modelPath = "C:\\Users\\bulle\\test_py\\best.onnx";
//        string imagePath = "C:\\Users\\bulle\\test_py\\new_img3.jpg";

//        // 1. 이미지 로드 및 원본 크기 저장
//        using Mat image = Cv2.ImRead(imagePath);
//        if (image.Empty())
//        {
//            Console.WriteLine("이미지를 불러올 수 없습니다.");
//            return;
//        }

//        int originalWidth = image.Width;
//        int originalHeight = image.Height;
//        int inputSize = 640; // YOLO 표준 입력 크기

//        // 2. 고속 전처리 (Blob 생성: 640x640 리사이즈, BGR->RGB, 0~1 정규화)
//        using Mat blob = CvDnn.BlobFromImage(
//            image,
//            scaleFactor: 1.0 / 255.0,
//            size: new OpenCvSharp.Size(inputSize, inputSize),
//            mean: new Scalar(0, 0, 0),
//            swapRB: true,
//            crop: false
//        );

//        // 💡 2-1. Blob 데이터를 C# 배열로 복사 후 텐서 생성 
//        int dimensionsSize = 1 * 3 * inputSize * inputSize;
//        float[] managedArray = new float[dimensionsSize];
//        System.Runtime.InteropServices.Marshal.Copy(blob.Data, managedArray, 0, dimensionsSize);

//        var inputTensor = new DenseTensor<float>(managedArray, new[] { 1, 3, inputSize, inputSize });

//        // 3. ONNX 추론 실행
//        using var session = new InferenceSession(modelPath);
//        string inputName = session.InputMetadata.Keys.First();
//        var inputs = new List<NamedOnnxValue> { NamedOnnxValue.CreateFromTensor(inputName, inputTensor) };

//        using var results = session.Run(inputs);
//        var outputTensor = results.First().AsTensor<float>(); // [1, 84, 8400]

//        // 4. 출력 텐서 파싱 및 바운딩 박스 추출
//        List<Rect> boxes = new List<Rect>();
//        List<float> confidences = new List<float>();
//        List<int> classIds = new List<int>();

//        float xFactor = (float)originalWidth / inputSize;
//        float yFactor = (float)originalHeight / inputSize;

//        int dimensions = 5; // 4 (좌표) + 80 (COCO 클래스 수)
//        int predictions = 8400;

//        for (int i = 0; i < predictions; i++)
//        {
//            // 클래스 점수들 중 가장 높은 값 찾기
//            float maxClassScore = outputTensor[0, 4, i];
//            int classId = 0; // 클래스가 하나이므로 ID는 항상 0

//            // 임계값(Confidence > 0.25)을 넘는 객체만 수집
//            if (maxClassScore > 0.25f)
//            {
//                float cx = outputTensor[0, 0, i];
//                float cy = outputTensor[0, 1, i];
//                float w = outputTensor[0, 2, i];
//                float h = outputTensor[0, 3, i];

//                int left = (int)((cx - w / 2) * xFactor);
//                int top = (int)((cy - h / 2) * yFactor);
//                int width = (int)(w * xFactor);
//                int height = (int)(h * yFactor);

//                boxes.Add(new Rect(left, top, width, height));
//                confidences.Add(maxClassScore);
//                classIds.Add(classId);
//            }
//        }

//        // 5. NMS(Non-Maximum Suppression)를 통한 겹치는 박스 제거
//        CvDnn.NMSBoxes(boxes, confidences, scoreThreshold: 0.25f, nmsThreshold: 0.45f, out int[] indices);

//        // 6. 결과 이미지에 박스 및 라벨 그리기
//        foreach (int i in indices)
//        {
//            Rect box = boxes[i];
//            float confidence = confidences[i];
//            int classId = classIds[i];


//            // 테두리 그리기 (초록색)
//            Cv2.Rectangle(image, box, Scalar.LimeGreen, 2);

//            // 라벨 텍스트 표시
//            string label = $"Class {classId}: {confidence:P0}";
//            Cv2.PutText(image, label, new OpenCvSharp.Point(box.X, Math.Max(box.Y - 10, 20)),
//                        HersheyFonts.HersheySimplex, 0.5, Scalar.LimeGreen, 2);
//        }

//        // 7. 화면에 띄우고 파일로 저장
//        Cv2.ImShow("YOLO Detection Result", image);
//        // Cv2.ImWrite("result_detected.jpg", image);

//        Console.WriteLine($"탐지 완료! 총 {indices.Length}개의 객체가 발견되었습니다. 아무 키나 누르면 종료됩니다.");
//        Cv2.WaitKey(0);
//        Cv2.DestroyAllWindows();
//    }
//}

//////////////////////////

using Microsoft.ML.OnnxRuntime;
using Microsoft.ML.OnnxRuntime.Tensors;
using OpenCvSharp;
using OpenCvSharp.Dnn;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;

class Program
{
    static void Main(string[] args)
    {
        string modelPath = "C:\\Users\\bulle\\test_py\\yolov8n.onnx";
        //string modelPath = "C:\\Users\\bulle\\test_py\\best.onnx";
        int inputSize = 640; // YOLO 표준 입력 크기

        // 1. ONNX 세션 열기
        using var session = new InferenceSession(modelPath);
        string inputName = session.InputMetadata.Keys.First();

        // 2. 웹캠 열기 (0번 카메라)
        using var capture = new VideoCapture(0);
        if (!capture.IsOpened())
        {
            Console.WriteLine("웹캠을 열 수 없습니다.");
            return;
        }

        // 카메라 해상도 설정 (필요에 따라 조절 가능)
        capture.Set(VideoCaptureProperties.FrameWidth, 1280);
        capture.Set(VideoCaptureProperties.FrameHeight, 720);

        Console.WriteLine("실시간 객체 탐지 시작 ('ESC' 키를 누르면 종료됩니다)");

        using Mat frame = new Mat();

        // 실시간 성능 최적화를 위해 텐서 메모리를 루프 바깥에서 한 번만 할당
        int dimensionsSize = 1 * 3 * inputSize * inputSize;
        float[] managedArray = new float[dimensionsSize];
        var inputTensor = new DenseTensor<float>(managedArray, new[] { 1, 3, inputSize, inputSize });

        Stopwatch stopwatch = new Stopwatch();

        while (true)
        {
            stopwatch.Restart();

            capture.Read(frame);
            if (frame.Empty()) break;

            int originalWidth = frame.Width;
            int originalHeight = frame.Height;

            // 3. 고속 전처리 (Blob 생성: 640x640 리사이즈, BGR->RGB, 0~1 정규화)
            using (Mat blob = CvDnn.BlobFromImage(
                frame,
                scaleFactor: 1.0 / 255.0,
                size: new OpenCvSharp.Size(inputSize, inputSize),
                mean: new Scalar(0, 0, 0),
                swapRB: true,
                crop: false
            ))
            {
                // 4. Blob 데이터를 미리 할당해 둔 배열에 복사
                System.Runtime.InteropServices.Marshal.Copy(blob.Data, managedArray, 0, dimensionsSize);
            }

            // 5. ONNX 추론 실행
            var inputs = new List<NamedOnnxValue> { NamedOnnxValue.CreateFromTensor(inputName, inputTensor) };
            using var results = session.Run(inputs);
            var outputTensor = results.First().AsTensor<float>(); // [1, 84, 8400]

            // 6. 출력 텐서 파싱 및 바운딩 박스 추출
            List<Rect> boxes = new List<Rect>();
            List<float> confidences = new List<float>();
            List<int> classIds = new List<int>();

            float xFactor = (float)originalWidth / inputSize;
            float yFactor = (float)originalHeight / inputSize;

            int dimensions = 84; // 4 (좌표) + 80 (COCO 클래스 수)
            int predictions = 8400;

            for (int i = 0; i < predictions; i++)
            {
                // 단일 클래스 
                float maxClassScore = outputTensor[0, 4, i];
                int classId = 0; // 클래스 ID (단일 클래스일 경우 0)

                //// 다중 클래스
                //float maxClassScore = 0;
                //int classId = -1;
                //for (int c = 4; c < dimensions; c++)
                //{
                //    float score = outputTensor[0, c, i];
                //    if (score > maxClassScore)
                //    {
                //        maxClassScore = score;
                //        classId = c - 4;
                //    }
                //}

                // 임계값(Confidence > 0.35)을 넘는 객체만 수집 (실시간은 떨림 방지를 위해 0.35~0.4 권장)
                if (maxClassScore > 0.35f)
                {
                    float cx = outputTensor[0, 0, i];
                    float cy = outputTensor[0, 1, i];
                    float w = outputTensor[0, 2, i];
                    float h = outputTensor[0, 3, i];

                    int left = (int)((cx - w / 2) * xFactor);
                    int top = (int)((cy - h / 2) * yFactor);
                    int width = (int)(w * xFactor);
                    int height = (int)(h * yFactor);

                    boxes.Add(new Rect(left, top, width, height));
                    confidences.Add(maxClassScore);
                    classIds.Add(classId);
                }
            }

            // 7.NMS(Non - Maximum Suppression)를 통한 겹치는 박스 제거
            CvDnn.NMSBoxes(boxes, confidences, scoreThreshold: 0.35f, nmsThreshold: 0.45f, out int[] indices);

            // 8. 결과 프레임에 박스 및 라벨 그리기
            foreach (int i in indices)
            {
                Rect box = boxes[i];
                float confidence = confidences[i];
                int classId = classIds[i];

                // 테두리 그리기 (초록색)
                Cv2.Rectangle(frame, box, Scalar.LimeGreen, 2);

                // 라벨 텍스트 표시
                string label = $"Class {classId}: {confidence:P0}";
                Cv2.PutText(frame, label, new OpenCvSharp.Point(box.X, Math.Max(box.Y - 10, 20)),
                            HersheyFonts.HersheySimplex, 0.5, Scalar.LimeGreen, 2);
            }


            // FPS 계산 및 화면 표시
            stopwatch.Stop();
            double fps = 1000.0 / stopwatch.ElapsedMilliseconds;
            Cv2.PutText(frame, $"FPS: {fps:F1}", new OpenCvSharp.Point(20, 40),
                        HersheyFonts.HersheySimplex, 1.0, Scalar.Yellow, 2);

            // 9. 결과 화면 출력 (ESC 키 누르면 종료)
            Cv2.ImShow("YOLO Realtime Detection", frame);
            if (Cv2.WaitKey(1) == 27) // 27은 ESC 키
            {
                break;
            }
        }

        Cv2.DestroyAllWindows();
        Console.WriteLine("실시간 탐지가 종료되었습니다.");
    }
}
