import json
from datetime import datetime


with open('survey.json', 'r') as f:
    surveys = json.load(f)

new_list = []
for survey in surveys:
    new_data = {'model': 'users.survey'}
    new_data['fields'] = survey
    new_data['fields']['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f%z')
    new_list.append(new_data)

with open('survey_data.json', 'w', encoding='UTF-8') as f:
    json.dump(new_list, f, ensure_ascii=False, indent=2)