import json
import re
from dsl.helper import *
from dsl.InterpreterJSON import *

class InterpreterDSL:
    
    def __init__(self, file_path, logs_path):
        self.file_path = file_path
        self.logs_path = logs_path

    def run(self):
        content = self.read_file()
        parsed_rules = self.parse_rule(content)
        matched_antipattern, missing_metrics = self.match_antipattern_template(parsed_rules)
        saved_path = self.create_rule_card(matched_antipattern, parsed_rules, missing_metrics, "./cards/json")
        self.main(saved_path)       
    
    def read_file(self):
        with open(self.file_path, 'r') as file:
          file_contents = file.read()
        return file_contents
    
    def parse_rule(self, content):
       parsed_rules = []
       rules = re.findall(r'rule\s+"[^"]+"\s*\{\s*when\s*(.*?)\s*;\s*then\s*', content, re.DOTALL)
       for rule in rules:
         service, condition = rule.strip().split('.')
         metric_id, ordi_value = condition.strip().split(' ', 1)
         comparator, value = self.extract_comparator_and_value(ordi_value)
         parsed_rules.append({
             "name": service,
             "metric_id": metric_id,
             "comparator": comparator,
             "num_value": value
         })
       return parsed_rules

    def extract_comparator_and_value(self,ordi_value):
        if ">=" in ordi_value:
            return "greater_equal", ordi_value.split(">=")[1].strip()
        elif "<=" in ordi_value:
            return "less_equal", ordi_value.split("<=")[1].strip()
        elif ">" in ordi_value:
            return "greater", ordi_value.split(">")[1].strip()
        elif "<" in ordi_value:
            return "less", ordi_value.split("<")[1].strip()
        elif "=" in ordi_value:
            return "equal", ordi_value.split("=")[1].strip()
        else:
            return None, ordi_value
        
    def match_antipattern_template(self, parsed_rules):
        # Извлечение metric_id из parsed_rules
        metric_ids = [rule['metric_id'] for rule in parsed_rules]
        
        # Преобразование идентификаторов метрик в элементы перечисления METRIC_ID
        metric_id_list = []
        for metric_id in metric_ids:
            for item in METRIC_ID:
                if item.value == metric_id:
                    metric_id_list.append(item)
                    break
        
        best_match = None
        best_match_percentage = 0
        missing_metrics = []

        for antipattern, metrics in Antipattern.__members__.items():
            matching_elements = set(metric_id_list).intersection(set(metrics.value))
            match_percentage = len(matching_elements) / len(metrics.value)
            
            if match_percentage >= 0.6 and match_percentage > best_match_percentage:
                best_match = antipattern
                best_match_percentage = match_percentage
                # Вычисление отсутствующих метрик для текущего лучшего совпадения
                missing_metrics = list(set(metrics.value) - matching_elements)
        return best_match, missing_metrics

    
    def create_rule_card(self, best_match, parsed_rules, missing_metrics, save_filepath):
        file_name = f"{best_match if best_match else 'No_match_found'}.json"
        full_path = f"{save_filepath}/{file_name}"

        for item in missing_metrics:
            parsed_rules.append({
             "name": "",
             "metric_id": item.value,
             "ordi_value": "high"
         })
            
        metric_ids = [rule['metric_id'] for rule in parsed_rules]
        
        parsed_rules.insert(0,  { 
            "name": best_match, 
            "operator": "INTER", 
            "rule_names": ", ".join(metric_ids)
        })
    
        # Создание содержимого JSON
        result_json = {
            "rule_card": best_match if best_match else "No match found",
            "rules": parsed_rules
        }
        
        # Сохранение JSON в файл
        with open(full_path, 'w') as json_file:
            json.dump(result_json, json_file, indent=2)

        return full_path

    def main(self, saved_path):

        interpreter = Interpretator(file=saved_path, logs_path=self.logs_path)
        interpreter.run()