import re
from typing import List, Dict


def quick_search(filename: str, search_term: str) -> List[Dict[str, str]]:
    """
    Выполняет быстрый поиск контактов по фрагменту слова в любом из полей контакта, включая ID.

    Args:
        filename (str): Путь к файлу с контактами.
        search_term (str): Поисковый запрос.

    Returns:
        List[Dict[str, str]]: Список найденных контактов, где каждый контакт представлен в виде словаря.
    """
    headers = ['ID', 'Фамилия', 'Имя', 'Отчество', 'Организация', 'Рабочий телефон', 'Личный телефон']
    found_contacts = []

    with open(filename, 'r', encoding='utf-8') as file:
        next(file)  # Пропускаем заголовок
        for line in file:
            contact = dict(zip(headers, line.strip().split(',')))
            if any(search_term.lower() in value.lower() for value in contact.values()):
                found_contacts.append(contact)

    return found_contacts


def precise_search(filename: str, **search_criteria) -> List[Dict[str, str]]:
    """
    Выполняет точный поиск контактов по заданным критериям, используя регулярные выражения.

    Args:
        filename (str): Путь к файлу с контактами.
        **search_criteria: Критерии поиска, где ключ - имя поля контакта, а значение - регулярное выражение для поиска.

    Returns:
        List[Dict[str, str]]: Список найденных контактов, соответствующих всем критериям поиска.
    """
    headers = ['ID', 'Фамилия', 'Имя', 'Отчество', 'Организация', 'Рабочий телефон', 'Личный телефон']
    found_contacts = []

    with open(filename, 'r', encoding='utf-8') as file:
        next(file)
        contacts = [dict(zip(headers, line.strip().split(','))) for line in file]

    for contact in contacts:
        match = True
        for field, pattern in search_criteria.items():
            if field == 'ID':
                if not re.search(f"^{pattern}$", contact.get(field, ""), re.IGNORECASE):
                    match = False
                    break
            else:
                if not re.search(pattern, contact.get(field, ""), re.IGNORECASE):
                    match = False
                    break
        if match:
            found_contacts.append(contact)

    return found_contacts
