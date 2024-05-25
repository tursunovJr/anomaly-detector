import random

class Processor:
  def pre_process_data(antipattern, data):
    result = []
    if antipattern == 'DuplicatedService':
      for row in data:
        tmp = (row[0], row[1], row[-1])
        result.append(tmp)
    elif antipattern == 'NobodyHome':
      for row in data:
        tmp = (row[0], row[2], row[-1])
        result.append(tmp)
    return result
