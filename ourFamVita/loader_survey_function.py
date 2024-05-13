import json


with open('survey_function.json', 'r') as f:
    functions = json.load(f)

new_list = []
for function in functions:
    new_data = {'model': 'users.surveyfunction'}
    new_data['fields'] = function
    new_list.append(new_data)

with open('survey_function_data.json', 'w', encoding='UTF-8') as f:
    json.dump(new_list, f, ensure_ascii=False, indent=2)