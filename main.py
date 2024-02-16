from contacts_delete import prompt_delete_or_refine_search
from contacts_display import read_contacts, display_contacts
from contacts_manage import add_contact, update_selected_contacts, organize_contacts
from contacts_search import quick_search, precise_search
from decorators import welcome_info_decorator


@welcome_info_decorator('contacts.csv')
def main_menu() -> None:
    """Основное меню программы управления контактами."""
    filename = 'contacts.csv'

    while True:
        print("\nФункционал:")
        print("0 - Показать все контакты")
        print("1 - Показать контакты по страницам")
        print("2 - Добавить контакт")
        print("3 - Редактировать контакт")
        print("4 - Быстрый поиск")
        print("5 - Фильтрация данных")
        print("6 - Удаление")
        print("7 - Выйти")
        print()
        choice = input("Выберите действие: ")
        print()

        # Вывод всех контактов
        if choice == '0':
            for contact in read_contacts(filename):
                print(', '.join(i for i in contact.values()))

        # Пагинация контактов
        elif choice == '1':
            while True:
                per_page = input("Введите количество записей на страницу или 'exit' для возврата в главное меню: ")
                if per_page.lower() == 'exit':
                    break  # Выход из текущего цикла, возврат в главное меню
                if not per_page.isdigit() or int(per_page) <= 0:
                    print("Введите корректное числовое значение для количества записей на страницу.")
                    continue  # Повторный запрос ввода количества записей на страницу
                while True:
                    page = input("Введите номер страницы или 'exit' для возврата в главное меню: ")
                    if page.lower() == 'exit':
                        break  # Выход из вложенного цикла, возврат в главное меню
                    if not page.isdigit() or int(page) <= 0:
                        print("Введите корректное числовое значение для номера страницы.")
                        continue  # Повторный запрос ввода номера страницы
                    display_contacts(filename, int(page), int(per_page))
                    break  # Выход из вложенного цикла после успешного выполнения
                break  # Выход из внешнего цикла после успешного выполнения или команды 'exit'

        # Добавление новых контактов
        elif choice == '2':
            while True:
                print("Введите данные новых контактов, разделяя каждый контакт символом '|'.")
                print("""Пример: Иванов,Иван,Иванович,ООО 'Рога и Копыта',+74951234567,+79161234567 | Петров,Петр,Петрович,ООО 'Копыта и Рога',+74957654321,+79167654321""")
                new_contacts_data = input("Введите данные или 'exit' для возврата в главное меню: ")
                if new_contacts_data.lower() == 'exit':
                    break  # Возврат в главное меню
                # Проверка валидности введенных данных
                if not new_contacts_data or not all(
                        len(contact.split(',')) == 6 for contact in new_contacts_data.split('|')):
                    print("Неверный формат данных, пожалуйста, следуйте примеру.")
                    continue
                add_contact(filename, new_contacts_data)
                break

        # Редактирование контактов
        elif choice == '3':
            update_selected_contacts(filename)

        # Быстрый поиск контактов
        elif choice == '4':
            while True:  # Добавляем цикл для возможности повторного поиска
                search_term = input("\nВведите фрагмент для быстрого поиска или 'exit' для возврата в меню: ")
                if search_term.lower() == 'exit':  # Проверка на команду выхода
                    break  # Выход из цикла, возврат в основное меню
                found_contacts = quick_search(filename, search_term)
                if found_contacts:
                    for contact in found_contacts:
                        print(', '.join(contact.values()))
                else:
                    print("По вашему запросу контакты не найдены.")

        # Фильтрация контактов
        elif choice == '5':
            while True:  # Добавляем цикл для возможности многократного использования фильтрации
                print("Фильтрация списка пользователей с использованием регулярных выражений.")
                print("Введите 'exit' для возврата в главное меню.")
                print("Примеры ввода критериев фильтрации:")
                print(r"  Фамилия=^Иванов - найдет всех пользователей, чья фамилия начинается на 'Иванов'")
                print(r"  Организация=.*ООО 'Рога и Копыта'.* - найдет всех, кто работает в 'ООО Рога и Копыта'")
                print("Введите критерии фильтрации в формате 'Поле=регулярное_выражение', разделяя критерии запятой:\n")
                search_criteria_input = input("Ваш запрос: ")
                print()
                if search_criteria_input.lower() == 'exit':
                    break  # Выход из цикла фильтрации, возврат в основное меню
                # Обработка ввода пользователя для поддержки множественных критериев
                try:
                    search_criteria = dict(item.split('=') for item in search_criteria_input.split(', '))
                except ValueError:
                    print("Ошибка в формате ввода. Пожалуйста, следуйте примеру:\n")
                    continue
                found_contacts = precise_search(filename, **search_criteria)
                if found_contacts:
                    for contact in found_contacts:
                        print(', '.join(contact.values()))
                    print()
                else:
                    print("По указанным критериям пользователи не найдены.\n")

        # Удаление контактов
        elif choice == '6':
            search_term = input("Введите информацию для поиска контакта для удаления или 'exit' для возврата в меню: ")
            if search_term.lower() == 'exit':
                continue  # Возврат в главное меню
            found_contacts = quick_search(filename, search_term)  # Использование быстрого поиска для нахождения контактов
            if found_contacts:
                # Убираем избыточный вывод информации о найденных контактах, поскольку он будет выполнен в функции prompt_delete_or_refine_search
                prompt_delete_or_refine_search(filename, found_contacts)
            else:
                print("Контакты не найдены.\n")

        # Выход из программы
        elif choice == '7':
            print("Выход из программы.")
            break

        # Организация контактов
        elif choice.lower() == 'organize':
            organize_contacts(filename)

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main_menu()
