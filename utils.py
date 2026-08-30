"""Shared normalization helpers."""


def normalize_tag(tag: str) -> str:
    """Return a normalized non-empty tag without a leading hash."""
    normalized_tag = tag.strip().lstrip("#").strip().lower()
    if not normalized_tag:
        raise ValueError("Тег не може бути порожнім.")
    return normalized_tag
