import sqlite3
from utils.csv import writeData
from utils.department import get_department
from utils.college import get_college

def getDptData():
  con = sqlite3.connect("data.db")
  con.row_factory = sqlite3.Row
  cursor = con.cursor()
  
  query = """
  SELECT id, unit, name, teacher, subNum
  FROM COURSE
  WHERE y = "111" AND s = "1";
  """

  req = cursor.execute(query)
  res = req.fetchall()
  
  datas = []
  
  for course in res:
    department_name = get_department(course["subNum"])
    print(department_name)
    college_name = get_college(department_name)
    print(college_name)
    datas.append({
      "question": f'課程代碼為{course["id"][4:-1]}，由{course["teacher"]}教授所開設的{course["name"]}是由哪個學院與學系開設的？',
      "answer": f'{course["teacher"]}教授所開設的{course["name"]}是由{college_name}的{department_name}開設的'
    })

  writeData("dataset.csv", datas)
