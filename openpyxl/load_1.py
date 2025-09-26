from openpyxl import load_workbook
import glob
import pandas as pd

cell_files = glob.glob('./*.xlsx')

school = []
amount = []

for store in cell_files:    # 다수의 파일
    wb = load_workbook(store)
    ws = wb.active
    
    for data in ws['A5':'B12']: # 파일이 여러개일시 범위지정하여 값 가져오기
        for cell in data:
            if cell.column == 1:
                if cell.value is not None:
                    school.append(cell.value)
            elif cell.column == 2:
                if cell.value != None:
                    amount.append(cell.value)
    
df = pd.DataFrame({    # 데이터 프레임에 값과 함께하여 생성
    '물품' : school, '수량' : amount
})
df = df.groupby('물품').sum()  # 물품의 각 품목 기준으로 수량값 더하여 품목 하나로 반환
    
df.to_excel("./종합.xlsx")
