from typing import Any

def check_config(config: dict[str, Any]) -> bool:
    if "style" not in config:
        print("Style list not found")
        return False
    if "langs" not in config:
        print("Langs list not found")
        return False
    if "directory" not in config:
        print("Directory not found")
        return False
    return True
