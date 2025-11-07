from typing import Any

def check_config(config: dict[str, Any]) -> bool:
    mandatory = ["style", "langs", "directory"]
    for entry in mandatory:
        if entry not in config:
            print(f"{entry} not found in config")
            return False
    return True
