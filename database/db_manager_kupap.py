from database.db_manager_articles import get_article_by_number, get_adjacent_article_number

DB_FILE = "kupap.db"

def get_kupap_article(number: str) -> dict | None:
    return get_article_by_number(DB_FILE, number)

def get_adjacent_kupap_number(number: str, direction: str) -> str | None:
    return get_adjacent_article_number(DB_FILE, number, direction)