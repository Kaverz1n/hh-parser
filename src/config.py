import os

from configparser import ConfigParser

FILE_NAME = 'database.ini'
FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), FILE_NAME)


def config(filepath=FILE_PATH, section="postgresql"):
    parser = ConfigParser()
    parser.read(filepath)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filepath))
    return db
