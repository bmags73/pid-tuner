import re
from pathlib import Path

# Regex to match lines like "set roll_p = 40" or "get yaw_d = 23.5"
BF_SET_RE = re.compile(r"^\s*(?:set|get)\s+(\S+)\s*=\s*(.+)\s*$", re.IGNORECASE)

def parse_bf_dump(path: Path) -> dict[str, float | int | str]:
    """
    Read a Betaflight CLI dump and return a mapping of config keys to their values.
    Numeric values are cast to float or int; everything else is left as string.
    """
    config: dict[str, float | int | str] = {}

    # Load the entire dump into memory
    text = path.read_text()
    for line in text.splitlines():
        match = BF_SET_RE.match(line)
        if not match:
            continue  # skip non-matching lines

        key, raw_value = match.groups()
        key = key.lower().strip()

        # Try parsing as integer or float
        raw_value = raw_value.strip()
        try:
            if "." in raw_value:
                value: float | int | str = float(raw_value)
            else:
                value = int(raw_value)
        except ValueError:
            # Fallback to string if numeric parsing fails
            value = raw_value

        config[key] = value

    return config
