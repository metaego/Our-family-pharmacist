import json


with open('survey_disease.json', 'r') as f:
    diseases = json.load(f)

new_list = []
for disease in diseases:
    new_data = {'model': 'users.surveydisease'}
    new_data['fields'] = disease
    new_list.append(new_data)

with open('survey_disease_data.json', 'w', encoding='UTF-8') as f:
    json.dump(new_list, f, ensure_ascii=False, indent=2)