from dsl.helper import *
from db.antipatternsMatcher import AntipatternsMatcher
from dsl.processor import Processor
import sqlite3
from openpyxl import Workbook
import os

class GeneratedService:
    def detect_antipattern_based_on_rules(self):
        antipattern = ''
        metrics_id = list(self.rules.keys())
        print(metrics_id)
        for item in Antipattern:
            if set(metrics_id) == set(item.value):
                antipattern = item.name
                break
        return antipattern
    
    def execute_query(self, antipattern):
        # Сделать передачу пути к БД снаружи
        conn = sqlite3.connect(self.logs_path)
        cursor = conn.cursor()
        
        query = AntipatternsMatcher.sql_queries[antipattern]

        # Выполняем SQL-запрос
        cursor.execute(query)

        # Получаем результаты запроса
        results = cursor.fetchall()

        # Закрываем соединение с базой данных
        conn.close()

        return results
    
    def result_process(self, result, antipattern):
        if antipattern == 'BottleneckService':
            pre_processed_data = Processor.pre_process_data(antipattern, result)
            self.write_to_file(antipattern, ["Operation_name", "CPL", "A", "RT"], pre_processed_data)
        elif antipattern == 'ChattyService':
            self.write_to_file(antipattern, ["Operation_name", "PLD", "RT"], result)
        elif antipattern == 'DuplicatedService':
            pre_processed_data = Processor.pre_process_data(antipattern, result)
            self.write_to_file(antipattern, ["Operation_name", "EventType", "ANIM"], pre_processed_data)
        elif antipattern == 'LostDataService':
            self.write_to_file(antipattern, ["Invocation_ID", "Operation_name", "RQ_num", "RS_SE_num"], result)
        elif antipattern == 'NobodyHome':
            pre_processed_data = Processor.pre_process_data(antipattern, result)
            self.write_to_file(antipattern, ["Operation_name", "NMI", "PLD"], pre_processed_data)
        elif antipattern == 'ServiceChain':
            pre_processed_data = Processor.pre_process_data(antipattern, result)
            self.write_to_file(antipattern, ["Operation_name", "NTMI", "A"], pre_processed_data)

    def write_to_file(self, antipattern, columns_name, data):
        # Создаем новый документ
        wb = Workbook()
        ws = wb.active

        # Названия столбцов
        ws.append(columns_name)

        # Записываем данные
        for row in data:
            ws.append(row)

        report_path = "./reports"

        if not os.path.exists(report_path):
            os.makedirs(report_path)

        # Сохраняем документ
        wb.save(f"{report_path}/{antipattern}_Result.xlsx")


    def __init__(self, name, operator, rules, logs_path):
        self.name = name
        self.operator = operator
        self.rules = rules
        self.logs_path = logs_path
        self.main()

    def main(self):
        antipattern = self.detect_antipattern_based_on_rules()
        query_result = self.execute_query(antipattern)
        self.result_process(query_result, antipattern)
