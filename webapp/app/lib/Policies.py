import re


def policy_validate_device_name(policy_config, device_name: str) -> bool:
    a = lambda v: v == "" or (isinstance(v, str) and 1 <= len(v.strip()) <= int(
        policy_config.get('max_device_name_len', 50)) and re.fullmatch(r'[a-zA-Z0-9 _\-]+',
                                                                              v.strip()) is not None)

    return a(device_name)