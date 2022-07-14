def shorten_pk(unique_id: str) -> str:
    return f"{unique_id[:3]}-{unique_id[-3:]}"


if __name__ == "__main__":
    unique = "1df678df9"
    assert shorten_pk(unique) == "1df-df9"
