import json


class Utils:
    CONFIG_DATA_PATH = None

    @staticmethod
    def set_config_data_path(path):
        Utils.CONFIG_DATA_PATH = path

    @staticmethod
    def get_config_data():
        with open(Utils.CONFIG_DATA_PATH, encoding='utf-8') as json_file:
            data = json.load(json_file)
            print(data)
            return data

    @staticmethod
    def read_file(path):
        with open(path, encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def split_list(list, parts):
        k, m = divmod(len(list), parts)
        return (list[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(parts))