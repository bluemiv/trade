import os, json


def __get_config(filename):
    try:
        config_file_path = os.path.join(os.path.dirname(__file__), f"../{filename}")
        with open(config_file_path, "r", encoding="utf-8") as f:
            return json.loads(f.read())
    except Exception as e:
        print("Couldn't open config file. error:", e)
        return None


def get_config():
    upbit = __get_config("upbit.config.json")
    bybit = __get_config("bybit.config.json")
    return {
        "upbit": upbit,
        "bybit": bybit,
    }
