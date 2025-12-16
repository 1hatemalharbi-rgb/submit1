def get_columns(rows: list[dict[str, str]]) -> list[str]:
    if not rows:
        return []
    return list(rows[0].keys())