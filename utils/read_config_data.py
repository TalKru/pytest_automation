import configparser
import os

#config_file_path = r"D:\dev\pytest_automation\configurations\config.ini"
config_file_path = os.path.abspath(os.curdir) + r"\configurations\config.ini"
config = configparser.RawConfigParser()
config.read(config_file_path)


def get_home_url():
    url = config.get('commonInfo', 'HOME_URL')
    return url


def get_email():
    url = config.get('commonInfo', 'email')
    return url


def get_password():
    url = config.get('commonInfo', 'password')
    return url


# if __name__ == '__main__':
#     print('Data from config.ini file:')
#     print(get_home_url())
#     print(get_email())
#     print(get_password())




