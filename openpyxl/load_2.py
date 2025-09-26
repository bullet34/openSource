from openpyxl import load_workbook
import pandas as pd

file = './예제.xlsx'

wb = load_workbook(file, data_only=True)    # 엑셀에 수식이 있는 경우 반영
ws = wb.active

name_list = []
value_list = []

for i in range(2, ws.max_row + 1):  # 파일이 하나일시 파일의 max_row까지만 값 가져오기
    name_list.append(ws.cell(i, 1).value)
    value_list.append(ws.cell(i, 2).value)
    

df = pd.DataFrame()  # 데이터프레임 정의

df["이름"] = name_list  # 데이터프레임 값 삽입
df["값"] = value_list

print(df)
