from contacts_display import read_contacts
from contacts_search import quick_search
from typing import List, Dict


def prompt_delete_or_refine_search(filename: str, found_contacts: List[Dict[str, str]]) -> None:
    """
    Предлагает пользователю удалить найденные контакты или уточнить поиск.

    :param filename: Имя файла, из которого будут удаляться контакты.
    :param found_contacts: Список словарей с найденными контактами.
    """
    while True:
        print("Найденные контакты:")
        for contact in found_contacts:
            print(f"ID: {contact['ID']}, {', '.join([f'{k}: {v}' for k, v in contact.items() if k != 'ID'])}")

        response = input(
            "Выберите действие:\n"
            "Y - Удалить все найденные контакты,\n"
            "N - Отмена,\n"
            "Введите ID контактов для удаления, разделенные запятой, для удаления конкретных контактов,\n"
            "или введите уточняющие данные для поиска: ").replace(' ', '').strip().lower()

        if response == 'y':
            delete_contact(filename, [contact['ID'] for contact in found_contacts])
            print(f"Удалено контактов: {len(found_contacts)}")
            break
        elif response == 'n':
            break
        elif all(char.isdigit() or char == ',' for char in response):  # Улучшенная проверка ввода
            ids_to_delete = response.split(',')
            delete_contact(filename, ids_to_delete)
            print(f"Удалено контактов: {len(ids_to_delete)}")
            break
        else:
            refined_found_contacts = quick_search(filename, response)
            if refined_found_contacts:
                print(f"Найдено записей: {len(refined_found_contacts)}")
                found_contacts = refined_found_contacts  # Обновляем список найденных контактов для возможного удаления
            else:
                print("По вашему запросу контакты не найдены. Попробуйте уточнить критерии поиска.")


def delete_contact(filename: str, found_contacts_ids: List[str]) -> None:
    """
    Удаляет контакты из файла по их идентификаторам.

    :param filename: Имя файла, из которого будут удаляться контакты.
    :param found_contacts_ids: Список идентификаторов контактов для удаления.
    """
    contacts = read_contacts(filename)
    contacts_to_keep = [contact for contact in contacts if contact['ID'] not in found_contacts_ids]

    write_contacts(filename, contacts_to_keep)


def write_contacts(filename: str, contacts: List[Dict[str, str]]) -> None:
    """
    Записывает обновленный список контактов обратно в файл.

    :param filename: Имя файла для записи.
    :param contacts: Список контактов для записи.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("ID,Фамилия,Имя,Отчество,Организация,Рабочий телефон,Личный телефон\n")  # Заголовок для удобства
        for contact in contacts:
            file.write(','.join([str(contact[key]) for key in
                                 ['ID', 'Фамилия', 'Имя', 'Отчество', 'Организация', 'Рабочий телефон',
                                  'Личный телефон']]) + '\n')
