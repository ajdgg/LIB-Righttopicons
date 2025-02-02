import json
from pathlib import Path


"""
xjiebot 文件操作
懒的写直接复制
获取自身路径下的文件
"""


def file_path(file):
    return Path(__file__).resolve().parent / file


class xj_file_handle:
    def __init__(self):
        pass

    def xj_file_reading(self, file_name: str, file_content: str = None):
        json_file_path_reading = file_path(file_name)
        try:
            with json_file_path_reading.open("r", encoding="utf-8") as json_file:
                loaded_data = json.load(json_file)
            if file_content is None:
                return loaded_data
            return loaded_data.get(file_content, None)
        except FileNotFoundError:
            print(f"File not found: {file_name}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from the file: {file_name}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def xj_file_change(self, file_name: str, file_key: str, file_content: str):
        json_file_path_change = file_path(file_name)
        try:
            with json_file_path_change.open("r", encoding="utf-8") as json_file:
                loaded_data = json.load(json_file)
        except FileNotFoundError:
            print(f"文件 {file_name} 未找到。")
            return
        except json.JSONDecodeError:
            print(f"{file_name} 文件内容不是有效的JSON格式。")
            return
        if file_key not in loaded_data:
            print(f"键 '{file_key}' 在文件中不存在。")
            return
        loaded_data[file_key] = file_content
        try:
            with json_file_path_change.open("w", encoding="utf-8") as json_file:
                json.dump(loaded_data, json_file, indent=4)
        except IOError as e:
            print(f"写入文件时发生错误: {e}")

    def get_keys_ending_with_key(self, json_data, key_suffix='_KEY'):
        try:
            json_file_path_reading = file_path(json_data)

            with open(json_file_path_reading, "r", encoding="utf-8") as json_file:
                loaded_data = json.load(json_file)

        except FileNotFoundError:
            print(f"Error: The file {json_file_path_reading} was not found.")
            return None

        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from file {json_file_path_reading}.")
            return None

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

        result = {}
        for key in loaded_data.keys():
            if key.endswith(key_suffix) and loaded_data[key]:
                result[key] = loaded_data[key]

        return result

    def read_filenames_with_pathlib(directory):
        path_obj = Path(directory)
        filenames = [file.name for file in path_obj.iterdir() if file.is_file()]
        return filenames
