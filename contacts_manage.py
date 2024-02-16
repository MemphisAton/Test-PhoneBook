import re
from typing import List, Dict, Union

from contacts_display import read_contacts


def generate_next_id(existing_contacts: List[Dict[str, str]]) -> str:
    """
    Генерирует следующий уникальный ID для нового контакта на основе существующих контактов.

    Args:
        existing_contacts (List[Dict[str, str]]): Список существующих контактов.
    Returns:
        str: Строка с новым уникальным ID.
    """
    if not existing_contacts:
        return "1"  # Возвращаем строку, если контактов нет
    last_id = int(existing_contacts[-1]['ID'])  # Преобразуем последний ID в число
    return str(last_id + 1)  # Возвращаем следующий ID как строку


def add_contact(filename: str, contacts_data: Union[str, List[Dict[str, str]]]) -> None:
    """
    Добавляет новые контакты в файл. Поддерживает два формата входных данных: строку и список словарей.

    Args:
        filename (str): Имя файла, куда будут добавлены контакты.
        contacts_data (Union[str, List[Dict[str, str]]]): Данные новых контактов. Может быть строкой,
            где контакты разделены символом '|', или списком словарей.

    Returns:
        None
    """
    existing_contacts = read_contacts(filename)
    next_id = max([int(contact['ID']) for contact in existing_contacts], default=0) + 1 if existing_contacts else 1

    new_contacts = []
    duplicates = 0

    # Обработка входных данных в зависимости от их типа
    if isinstance(contacts_data, str):
        contacts_list = [
            dict(zip(['Фамилия', 'Имя', 'Отчество', 'Организация', 'Рабочий телефон', 'Личный телефон'],
                     contact.strip().split(',')))
            for contact in contacts_data.split('|')
            if len(contact.strip().split(',')) == 6
        ]
    elif isinstance(contacts_data, list) and all(isinstance(contact, dict) for contact in contacts_data):
        contacts_list = contacts_data
    else:
        print("Некорректный формат входных данных.")
        return

    for contact in contacts_list:
        # Добавляем ID только новым контактам, если ID не задан
        contact['ID'] = contact.get('ID', str(next_id))

        # Проверка на дубликаты без учета ID
        if any(all(contact[k] == existing[k] for k in contact if k != 'ID') for existing in existing_contacts):
            duplicates += 1
        else:
            new_contacts.append(contact)
            next_id = int(contact['ID']) + 1  # Подготовка ID для следующего контакта

    # Запись новых контактов в файл
    with open(filename, 'a', encoding='utf-8') as file:
        for contact in new_contacts:
            file.write(','.join([contact['ID']] + [contact[k] for k in
                                                   ['Фамилия', 'Имя', 'Отчество', 'Организация', 'Рабочий телефон',
                                                    'Личный телефон']]) + '\n')

    print(f"Добавлено контактов: {len(new_contacts)}.")
    if duplicates:
        print(f"Обнаружено дублирующихся контактов: {duplicates}, они не были добавлены.")


def update_selected_contacts(filename: str) -> None:
    """
    Позволяет пользователю выбрать и редактировать контакты по заданным критериям поиска.

    Args:
        filename (str): Имя файла с контактами.

    Returns:
        None
    """
    all_contacts = read_contacts(filename)

    # Поиск контактов
    search_query = input("Введите данные для поиска контактов, которые хотите редактировать: ")
    found_contacts = [contact for contact in all_contacts if search_query.lower() in ' '.join(contact.values()).lower()]

    if found_contacts:
        print("Найденные контакты:")
        for i, contact in enumerate(found_contacts, 1):
            print(
                f"{i}. ID: {contact['ID']}, Фамилия: {contact['Фамилия']}, Имя: {contact['Имя']}, Отчество: {contact['Отчество']}, Организация: {contact['Организация']}, Рабочий телефон: {contact['Рабочий телефон']}, Личный телефон: {contact['Личный телефон']}")

        while True:
            selection_input = input(
                "Введите номера контактов для редактирования через запятую без пробелов, 'ALL' для всех, 'exit' для выхода: ").strip()

            if selection_input.lower() == 'exit':
                return
            elif selection_input.lower() == 'all':
                selected_contacts = found_contacts
                break
            elif re.match(r'^\d+(,\d+)*$',
                          selection_input):  # Проверка на соответствие паттерну: одно число или числа через запятую без пробелов
                selected_indices = [int(index) - 1 for index in selection_input.split(',')]
                if all(0 <= index < len(found_contacts) for index in selected_indices):
                    selected_contacts = [found_contacts[index] for index in selected_indices]
                    break
                else:
                    print("Введенные номера выходят за пределы списка найденных контактов. Попробуйте снова.")
            else:
                print("Некорректный ввод. Убедитесь, что вводите номера через запятую без пробелов. Попробуйте снова.")

        updates = {}
        for field in ['Фамилия', 'Имя', 'Отчество', 'Организация', 'Рабочий телефон', 'Личный телефон']:
            new_value = input(f"Введите новое значение для {field} (оставьте пустым, если не хотите менять): ")
            if new_value:
                updates[field] = new_value

        for contact in selected_contacts:
            for key, new_value in updates.items():
                contact[key] = new_value

        save_updated_contacts(filename, all_contacts)
        print("Контакты были успешно обновлены.")
    else:
        print("Контакты не найдены.")


def save_updated_contacts(filename: str, contacts: List[Dict[str, str]]) -> None:
    """
    Сохраняет обновленный список контактов в файл.

    Args:
        filename (str): Имя файла для сохранения.
        contacts (List[Dict[str, str]]): Обновленный список контактов для сохранения.

    Returns:
        None
    """
    with open(filename, 'w', encoding='utf-8') as file:
        # Предполагается наличие заголовка в файле
        file.write("ID,Фамилия,Имя,Отчество,Организация,Рабочий телефон,Личный телефон\n")
        for contact in contacts:
            file.write(','.join(
                [contact['ID'], contact['Фамилия'], contact['Имя'], contact['Отчество'], contact['Организация'],
                 contact['Рабочий телефон'], contact['Личный телефон']]) + '\n')


def organize_contacts(filename: str) -> None:
    """
    Организует контакты в файле, сортируя их по фамилии и имени, и присваивает новые ID с начала.

    Args:
        filename (str): Имя файла с контактами.

    Returns:
        None
    """
    contacts = read_contacts(filename)
    # Сортировка контактов по Фамилии, а затем по Имени
    sorted_contacts = sorted(contacts, key=lambda x: (x['Фамилия'], x['Имя']))

    # Переназначение ID, начиная с 1
    for i, contact in enumerate(sorted_contacts, start=1):
        contact['ID'] = str(i)

    # Сохранение организованных контактов обратно в файл
    save_updated_contacts(filename, sorted_contacts)
    print("Контакты были успешно организованы.")
