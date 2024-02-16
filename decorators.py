def welcome_info_decorator(filename):
    def decorator(func):
        def wrapper(*args, **kwargs):
            ascii_art = [
                "                                          :+=     ",
                "                                      :+#%%=      ",
                "                                   .=###%+:       ",
                "                                  =%%#%*:         ",
                "          ..       ..       .:---#@#%@+           ",
                "          =--======----:  .:.  =@%#@%--=          ",
                "       .::=             .      #%#@%:  :=-.       ",
                "       =#=.             :.     +#%*:    +%=       ",
                "      .**=              -:     -:       =#*.      ",
                "      =#==              --    =-        .*#=      ",
                "     .*%=.              =-    :          +%*      ",
                "     =*++               =:               -**-     ",
                "     *%=-               =:               .*%+     ",
                "    -*#+                -:                +#*-    ",
                "    *#++   .:------:.   :.     ..:::::..  -*#*    ",
                "   :*%==--====++++++*+=:..:=+*###****+++++++%*:   ",
                "   **@%%%@@@@@@@@@@@@@@#--#@@@@@@@@@@@@@@@@%@**   ",
                "  .#*##########*******+=  -=+++++++++++++****+*.  ",
                "  .------------::::::::+===::::::::-----------=:  "
            ]

            # Получаем количество записей в файле
            num_records = 0
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    num_records = sum(1 for _ in file)
            except FileNotFoundError:
                num_records = "Файл не найден"

            # Информация о программе
            program_info = f"Название: Телефонный справочник\n\nВерсия: 1.0\n\nЗаписей в справочнике: {num_records}"

            max_art_width = max(len(line) for line in ascii_art)

            info_lines = program_info.split('\n')

            info_padding_top = (len(ascii_art) - len(info_lines)) // 2
            info_lines = [""] * info_padding_top + info_lines + [""] * (
                    len(ascii_art) - len(info_lines) - info_padding_top)

            for art_line, info_line in zip(ascii_art, info_lines):
                print(f"{art_line:<{max_art_width}}    {info_line}")

            return func(*args, **kwargs)

        return wrapper

    return decorator

