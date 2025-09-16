// notepad 작성

@ECHO ON

title start_test

cd C:\Users\project  // 실행파일 경로

call project_test/scripts/activate  // 가상환경의 인터프리터 지정
python test1.py  // test1.py 실행

cmd.exe
