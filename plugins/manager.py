import json
import os
import sys
import importlib

from multiprocessing import Pool, cpu_count


# DEFAULT PLUGIN
def default(name):
    print("Unknown command!")


default_plugin = {
    "name" : "Default Plugin",
    "simple_name" : "default",
    "version" : 1.0,
    "author" : "Jack Clarke",
    "description" : "Is executed when no other condition are met, a default case.",

    "code" : {
        "entry_point" : "test"
    }
}



# LOAD CONFIG FILES
def load_config(file):   # Loads a json file and checks if active flag is true, then returns it.
    print("Loading " + file + "...")
    with open(file, "r") as f:
        f = json.load(f)
        if f["active"]:
            print("    Loaded " + file + "!")
            return f

    return None


def load_configs(pool, directory):   # Finds all json files in a directory and maps the above function to multiple processes.
    configs = []

    if directory[-1] != "/":
        directory += "/"

    files = [directory + x for x in os.listdir(directory)]

    configs = [x for x in pool.map(load_config, files) if x is not None]

    return configs









# IMPORT CODE FILES
def import_plugin(config):  # Import single code file using json config.

    return {
        "name" : config["name"],
        "simple_name" : config["simple_name"],
        "author" : config["author"],
        "version" : config["version"],
        "description" : config["description"],
        "listen_for" : config["listen_for"],
        "function" : getattr(importlib.import_module(config["code"]["file"]), config["code"]["entry_point"])
    }

def import_plugins(pool, configs):
    return pool.map(import_plugin, configs)







# PLUGIN MANAGER CLASS
class PluginManager():
    def __init__(self, directory):
        pool = Pool(cpu_count())

        self.configs = load_configs(pool, directory)
        self.plugins = import_plugins(pool, self.configs)

        self.func_map = {x["listen_for"]:x["function"] for x in self.plugins}
        self.simple_name_map = {x["simple_name"]:x for x in self.plugins}


    def call(self, listen_for, *args, **kwargs):
        try:
            self.func_map[listen_for](*args, **kwargs)
        except KeyError:
            default()


    def info(self, simple_name):
        for key, val in self.simple_name_map[simple_name].items():
            print(str(key).capitalize() + " : " + str(val))





if __name__ == "__main__":
    plugman = PluginManager("plugin_config")

    plugman.call("testing shit", "porn camel")
    plugman.info("test_plugin")