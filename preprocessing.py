import os
import json

def preprocessing(path):
    file_list = os.listdir(path)

    merged_dict = {}

    for file_name in file_list:
        file_path = os.path.join(path, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = json.load(f)
            merged_dict[file_name] = file_content

    with open('merged_by_filename.json', 'w', encoding='utf-8') as out_f:
        json.dump(merged_dict, out_f, ensure_ascii=False, indent=2)

    file_names = [info['FILE'][0]['FILE_NAME'] for info in merged_dict.values()]

    file_items = []
    for i in range(len(file_list)):
        print(merged_dict[file_list[i]]['FILE'][0]['ITEMS'])
        file_items.append(merged_dict[file_list[i]]['FILE'][0]['ITEMS'])

    data_final = dict(zip(file_names, file_items))

    with open('data_final.json', 'w', encoding='utf-8') as out_f:
        json.dump(data_final, out_f, ensure_ascii=False, indent=2)

path = './labeling/big_truck/x'

preprocessing(path)