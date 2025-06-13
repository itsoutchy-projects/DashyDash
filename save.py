import json
import logger

def save_file(scene = 0):
    try:
        this_save = {
            "scene": scene,
            "playercol": "red",
            "dummylmao": {
                "dumb": 0,
                "letsgo": 5
            },
            "generated_by": "itsoutchy"
        }
        json_obj = json.dumps(this_save, indent=4)
        with open("save_1.json", "w") as f:
            f.write(json_obj)
    except Exception as e:
        logger.crash(e)