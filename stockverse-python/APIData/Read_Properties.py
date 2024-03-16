import configparser
import os 

#Accepts a property name value, searches for the property in the properties file and returns the value of the property
def load_properties(propName):
    current_dir = os.path.dirname(__file__)
    propFilePath = os.path.abspath(os.path.join(current_dir, "..", "properties","stockverse-python.properties"))
    config = configparser.ConfigParser()
    config.read(propFilePath)
    properties = {}
    for section in config.sections():
        for key, value in config.items(section):
            if(key == propName):
                return value
