# 다양한 파일 형식 읽기 예제
import pandas as pd
# CSV 파일 읽기
df_csv = pd.read_csv('data.csv')

# Excel 파일 읽기
df_excel = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# JSON 파일 읽기
df_json = pd.read_json('data.json')

# SQL 데이터베이스에서 읽기
# import sqlite3
# conn = sqlite3.connect('database.db')
# df_sql = pd.read_sql('SELECT * FROM table_name', conn)

# 여러 파일 형식으로 저장
# df.to_csv('output.csv', index=False)
# df.to_excel('output.xlsx', index=False)
# df.to_json('output.json')
