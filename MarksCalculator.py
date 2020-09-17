import csv
import json
import os


class MarksCalculator:
    def __init__(self, resultDir='./results'):
        self.resultDir = resultDir
        self.students = []
        self.resultFiles = [f'{resultDir}/{basename}' for basename in os.listdir(resultDir)]

    def cumulateResults(self):
        # print(self.resultFiles)
        for file in self.resultFiles:
            with open(file, 'r') as fh:
                self.processJson(json.load(fh))

    def processJson(self, json):
        names = json.get('names')
        # short title for each week
        title = json.get('title')[9:]

        for name in names:
            try:
                student = next(student for student in self.students if name == student['name'])
                # print(student)
                student['count'] += 1
                student['weeks'].append(title)
            except StopIteration:
                self.students.append({
                    'name': name,
                    'count': 1,
                    'weeks': [title]
                })
        for student in self.students:
            student['weeks'].sort()


