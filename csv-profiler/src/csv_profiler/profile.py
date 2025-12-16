MISSING = {"", "na", "n/a", "null", "none", "nan"}

def is_missing(value: str | None) -> bool:
    if value is None:
        return True
    return value.strip().casefold() in MISSING

def try_float(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None

def column_values(rows: list[dict[str, str]], col: str) -> list[str]:
    """Return all values of a column from the list of rows."""
    return [row.get(col, "") for row in rows]

def infer_type(values: list[str]) -> str:
    usable = [v for v in values if not is_missing(v)]
    if not usable:
        return "text"
    for v in usable:
        if try_float(v) is None:
            return "text"
    return "number"

def numeric_stats(values: list[str]) -> dict:
    usable = [v for v in values if not is_missing(v)]
    missing = len(values) - len(usable)
    nums: list[float] = []
    for v in usable:
        x = try_float(v)
        if x is None:
            raise ValueError(f"Non-numeric value found: {v!r}")
        nums.append(x)
        
    count = len(nums)
    unique = len(set(nums))
    return {
        "count": count,
        "missing": missing,
        "unique": unique,
        "min": min(nums) if nums else None,
        "max": max(nums) if nums else None,
        "mean": sum(nums) / count if count else None,
    }

def text_stats(values: list[str], top_k: int = 5) -> dict:
    usable = [v for v in values if not is_missing(v)]
    missing = len(values) - len(usable)
    counts: dict[str, int] = {}

    for v in usable:
        counts[v] = counts.get(v, 0) + 1

    top_items = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
    top = [{"value": v, "count": c} for v, c in top_items[:top_k]]

    return {
        "count": len(usable),
        "missing": missing,
        "top": top,
    }


def basic_profile(rows: list[dict[str, str]]) -> dict:
    if not rows:
        return {"rows": 0, "columns": {}, "notes": ["Empty dataset"]}

    columns = list(rows[0].keys())
    missing = {c: 0 for c in columns}
    non_empty = {c: 0 for c in columns}

    for row in rows:
        for c in columns:
            v = (row.get(c) or "").strip()
            if v == "":
                missing[c] += 1
            else:
                non_empty[c] += 1

    columns_profile: dict[str, dict] = {}
    for c in columns:
        values = column_values(rows, c)
        col_type = infer_type(values)

        if col_type == "number":
            stats = numeric_stats(values)
            columns_profile[c] = {
                "type": col_type,
                "count": stats["count"],
                "missing": stats["missing"],
                "unique": stats["unique"],
                "min": stats["min"],
                "max": stats["max"],
                "mean": stats["mean"],
            }
        else:
            stats = text_stats(values)
            columns_profile[c] = {
                "type": col_type,
                "count": stats["count"],
                "missing": stats["missing"],
                "unique": len(set(values)),
                "top": stats["top"],
            }

    return {
        "rows": len(rows),
        "n_cols": len(columns),
        "columns": columns_profile,
        "missing": missing,
        "non_empty": non_empty,
    }