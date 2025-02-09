import configparser
import os

# config_file_path = r"D:\dev\pytest_automation\configurations\config.ini"
# config_file_path = os.path.abspath(os.curdir) + r"\configurations\config.ini"
# Compute the path relative to this file's location
config_file_path = os.path.join(os.path.dirname(__file__), "..", "configurations", "config.ini")
config = configparser.RawConfigParser()
config.read(config_file_path)


def get_home_url():
    try:
        url = config.get('commonInfo', 'HOME_URL')
        return url

    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        raise Exception(f"Error reading HOME_URL from config: {e}")


def get_email():
    try:
        url = config.get('commonInfo', 'email')
        return url

    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        raise Exception(f"Error reading email from config: {e}")


def get_password():
    try:
        url = config.get('commonInfo', 'password')
        return url

    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        raise Exception(f"Error reading password from config: {e}")


if __name__ == '__main__':
    print('Data from config.ini file:')
    print(get_home_url())
    print(get_email())
    print(get_password())




