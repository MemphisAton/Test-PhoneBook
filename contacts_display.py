from typing import List, Dict


def read_contacts(filename: str) -> List[Dict[str, str]]:
    """
    Читает контакты из файла и возвращает список словарей, где каждый словарь представляет отдельный контакт.

    Args:
        filename (str): Путь к файлу с контактами.

    Returns:
        List[Dict[str, str]]: Список контактов, где каждый контакт представлен в виде словаря.
    """
    contacts = []
    with open(filename, 'r', encoding='utf-8') as file:
        next(file)  # Пропускаем заголовок файла
        for line in file:
            parts = line.strip().split(',')
            contact_dict = {
                'ID': parts[0],
                'Фамилия': parts[1],
                'Имя': parts[2],
                'Отчество': parts[3],
                'Организация': parts[4],
                'Рабочий телефон': parts[5],
                'Личный телефон': parts[6],
            }
            contacts.append(contact_dict)
    return contacts


def display_contacts(filename: str, page: int = 1, per_page: int = 5) -> None:
    """
    Отображает контакты, разбивая их на страницы для удобства просмотра.

    Args:
        filename (str): Путь к файлу с контактами.
        page (int): Номер страницы для отображения. По умолчанию равен 1.
        per_page (int): Количество контактов на одной странице. По умолчанию равно 5.

    Returns:
        None
    """
    contacts = read_contacts(filename)
    total_records = len(contacts)
    total_pages = -(-total_records // per_page)  # Округление вверх

    if page > total_pages or page < 1:
        print("Нет такой страницы.")
        return

    print(f"\nСтраница {page} из {total_pages}:")
    start_index = (page - 1) * per_page
    end_index = min(start_index + per_page, total_records)

    for contact in contacts[start_index:end_index]:
        contact_info = ', '.join([f'{key}: {value}' for key, value in contact.items()])
        print(contact_info)
