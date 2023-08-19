import sqlite3
from utils.time import getSessionArray, weekdayCode
from utils.csv import writeData

def getTimeData():
  con = sqlite3.connect("data.db")
  con.row_factory = sqlite3.Row
  cursor = con.cursor()
  
  req = cursor.execute("SELECT id, time, name, teacher FROM COURSE WHERE y = \"112\" AND s = \"1\"")
  res = req.fetchall()
  
  datas = []
  
  for course in res:
    sessionArray = getSessionArray(course["time"])
    if len(sessionArray) > 0:
      timeStr = ""
      for i, session in enumerate(sessionArray):
        if i == len(sessionArray) - 1 and i != 0:
          timeStr += "及"
        elif i > 0:
          timeStr += ", "
        timeStr += f'禮拜{weekdayCode[session["week_code"] - 1]}的{session["start_time"]}點到{session["end_time"]}點'
      datas.append({
        "question": f'課程代碼為{course["id"][4:-1]}，由{course["teacher"]}教授所開設的{course["name"]}上課時間是甚麼時候？',
        "answer": f'{timeStr}'
      })

  writeData("dataset.csv", datas)