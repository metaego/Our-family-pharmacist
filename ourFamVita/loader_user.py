import json
from datetime import datetime, timedelta


with open('user.json', 'r') as f:
    users = json.load(f)

new_list = []
for user in users:
    new_data = {'model': 'users.user'}
    new_data['fields'] = user
    new_data['fields']['custom_created_at'] = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d %H:%M:%S.%f%z')
    new_list.append(new_data)

with open('user_data.json', 'w', encoding='UTF-8') as f:
    json.dump(new_list, f, ensure_ascii=False, indent=2)