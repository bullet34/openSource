# pip install python-docx
# 폰트 설치

from docx import Document
import docx
from docx.oxml.ns import qn

#문서객체 생성
doc = Document('파일양식.docx')

#문서양식내에 단락 내용 확인
for i, paragraph in enumerate(doc.paragraphs):
    print(str(i) + ": " + paragraph.text)

#내용 수정
doc.paragraphs[3].clear()  # 3번째 단락 내용 지우기
run = doc.paragraphs[3].add_run('~ 내용 ~')  # 3번째 단락 내용 삽입
run.font.name ='나눔고딕'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '나눔고딕')
run.font.size = docx.shared.Pt(20)

#저장
doc.save('파일이름.docx')
