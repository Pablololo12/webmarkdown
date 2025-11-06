import yaml
import argparse
from .checkpointer import Checkpointer
from .config_check import check_config
from .worker import generate_html
from typing import Any

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean", action="store_true", help="Cleans the html")
    return parser.parse_args()

def get_project_config() -> dict[str, Any]:
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)
    return {}

def main():
    args = get_arguments()
    conf = get_project_config()
    chk = Checkpointer()
    if not check_config(conf):
        print("Error in the config")
        return
    try:
        if args.clean:
            chk.mrproper()
        else:
            generate_html(conf)
            chk.write()
    except Exception as e:
        print(f"Error: {e}")
        chk.write()



if __name__=="__main__":
    main()
