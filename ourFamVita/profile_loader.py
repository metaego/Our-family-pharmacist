import json
from datetime import datetime


with open('profile.json', 'r') as f:
    profiles = json.load(f)

new_list = []
for profile in profiles:
    new_data = {'model': 'users.profile'}
    new_data['fields'] = profile
    new_data['fields']['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f%z')
    new_list.append(new_data)

with open('profile_data.json', 'w', encoding='UTF-8') as f:
    json.dump(new_list, f, ensure_ascii=False, indent=2)