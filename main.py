from process.time import getTimeData
from process.department_college import getDptData
from utils.csv import writeData

if __name__ == "__main__":
  data = getTimeData() + getDptData()
  writeData("dataset.csv", data)