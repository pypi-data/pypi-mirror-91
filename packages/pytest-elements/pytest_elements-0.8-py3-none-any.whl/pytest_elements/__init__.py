_global_driver_map = {}


def set_driver(key, driver):
    global _global_driver_map
    _global_driver_map[key] = driver


def get_driver(key="default"):
    return _global_driver_map.get(key, None)
