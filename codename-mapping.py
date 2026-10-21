#!/usr/bin/env python3

import re
import json
import os

def parse_bash_script(script_path):
    """
    Извлечение номеров кейсов и имен пользователей из bash-скрипта
    """
    case_pattern = re.compile(r'(\d+)\)\n\s*user=(\w+)', re.MULTILINE)
    echo_pattern = re.compile(r'(\d+)\s*-\s*(.+)', re.MULTILINE)  # Обновлено регулярное выражение
    
    cases = {}
    echo_mappings = {}

    with open(script_path, 'r') as f:
        script_content = f.read()

        # Извлекаем сопоставления номеров и пользователей из блока case
        case_matches = case_pattern.findall(script_content)
        for case_num, user in case_matches:
            cases[int(case_num)] = user

        # Извлекаем кодовые имена из echo
        echo_matches = echo_pattern.findall(script_content)
        for echo_num, code_name in echo_matches:
            echo_mappings[int(echo_num)] = code_name.strip()  # Убираем лишние пробелы

    return cases, echo_mappings

def create_user_mappings(cases, echo_mappings):
    """
    Сопоставление кодовых имен с пользователями на основе номеров кейсов
    """
    user_mappings = {}
    for case_num, user in cases.items():
        if case_num in echo_mappings:
            user_mappings[user] = echo_mappings[case_num]
        else:
            print(f"Предупреждение: Для кейса {case_num} не найдено кодовое имя в echo")

    return user_mappings

def main():
    # Получаем домашнюю директорию текущего пользователя
    home_dir = os.path.expanduser("~")

    # Путь к файлу run.file в домашней папке
    script_path = os.path.join(home_dir, "run.file")

    # Парсим скрипт для получения пользователей и кодовых имен
    cases, echo_mappings = parse_bash_script(script_path)

    # Сопоставляем кодовые имена с пользователями
    user_mappings = create_user_mappings(cases, echo_mappings)

    # Путь к выходному файлу в домашней папке
    output_file = os.path.join(home_dir, ".user_mappings.json")

    # Сохраняем результат в JSON файл
    with open(output_file, 'w') as f:
        json.dump(user_mappings, f, indent=4)

    print(f"Сопоставление кодовых имен сохранено в {output_file}")

if __name__ == "__main__":
    main()
