import json
import os


def get_file_name(file_path):
    return file_path.split('/')[-1]

def make_result_json( data, output_path="output/result.json"):
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)