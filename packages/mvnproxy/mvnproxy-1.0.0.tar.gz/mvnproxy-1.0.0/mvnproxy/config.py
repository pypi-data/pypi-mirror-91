from typing import cast, Dict
import addict
import yaml

with open("config.yml", "rt", encoding="utf-8") as f:
    data = addict.Dict(cast(Dict, yaml.safe_load(f)))

cache_folder = data.get("cache_folder", "/tmp/mvnproxy")
host = data.get("host", "0.0.0.0")
port = int(data.get("port", 7000))
