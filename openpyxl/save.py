import pandas as pd


a = """
1번 30
2번 22
3번 11
4번 23
5번 93  
6번 24
7번 29
"""

name_list = []
value_list = []

a = a.strip().split('\n')

for i in a:
    name, value = i.split()
    name_list.append(name)
    value_list.append(value)

# 합산 값
ab = sum(map(int, value_list))
name_list.append("총")
value_list.append(ab)


df = pd.DataFrame({
    '이름':name_list,
    '값':value_list,
})

print(df)
df.to_excel("./예제.xlsx", index=False) # 저장시 인덱스 제외. 예시) 1  이름  값 
                                                                # 2 이름 값
