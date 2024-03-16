import configparser
import os

#Accepts a property name value, searches for the property in the properties file and returns the value of the property
def load_properties(prop_name):
    current_dir = os.path.dirname(__file__)
    prop_file_path = os.path.abspath(os.path.join(current_dir, "..", "properties", "stockverse-python.properties"))
    config = configparser.ConfigParser()
    config.read(prop_file_path)

    for section in config.sections():
        for key, value in config.items(section):
            if key == prop_name:
                return value
