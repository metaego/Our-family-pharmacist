import json


with open('survey_allergy.json', 'r') as f:
    allergys = json.load(f)

new_list = []
for allergy in allergys:
    new_data = {'model': 'users.surveyallergy'}
    new_data['fields'] = allergy
    new_list.append(new_data)

with open('survey_allergy_data.json', 'w', encoding='UTF-8') as f:
    json.dump(new_list, f, ensure_ascii=False, indent=2)