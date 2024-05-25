import json
from dsl.helper import *
from dsl.GeneratedService import GeneratedService

class Interpretator:

  def __init__(self, file, logs_path):
    self.file = file
    self.logs_path = logs_path

  def is_boolean_string(self, value):
      return value.lower() in ["true", "false"]

  def convert_to_bool(self, value):
      return value.lower() == "true"
      

  def run(self):
    with open(self.file, "r") as file:
      data = json.load(file)

      # Начинаем формировать содержимое нового Python файла
      class_name = data['rule_card']
      operator = data['rules'][0]['operator']  # Предполагаем, что оператор указан для первого правила

      rules_dict = dict()


      for rule in data['rules']:
        if 'metric_id' in rule:
            if rule.get('ordi_value') is not None:
                rules_dict[METRIC_ID(rule['metric_id'])] = Ordi_Value(rule['ordi_value'])
            elif rule.get('num_value') is not None:
                num_value = rule['num_value']
                if self.is_boolean_string(num_value):
                    rules_dict[METRIC_ID(rule['metric_id'])] = self.convert_to_bool(num_value)
                else:
                    try:
                        # Попробуем преобразовать к целому числу
                        rules_dict[METRIC_ID(rule['metric_id'])] = int(num_value)
                    except ValueError:
                        try:
                            # Если не получилось, попробуем преобразовать к дробному числу
                            rules_dict[METRIC_ID(rule['metric_id'])] = float(num_value)
                        except ValueError:
                            raise ValueError(f"Unsupported num_value: {num_value}")



      generatedService = GeneratedService(
        name = class_name,
        operator = operator,
        rules=rules_dict,
        logs_path=self.logs_path
      )

  