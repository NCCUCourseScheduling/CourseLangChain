import csv, os

###
# 
###
def writeData(filename: str, data: list, header: list = ['question', 'answer'] ):
  """Write data to csv file

  Args:
      filename (str): file name.
      data (list): data, which will be list of dictionary.
      header (list, optional): csv header. Defaults to ['question', 'answer'].
  """
  with open(os.path.join(os.getcwd(), filename), 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header)
    writer.writeheader()
    for data in data:
      writer.writerow(data)