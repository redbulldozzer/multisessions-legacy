#!/bin/bash

# Функция для проверки наличия пакета
check_and_install_package() {
    package=$1
    dpkg -l | grep -qw "$package" || sudo apt install -y "$package"
}

# Проверка и установка зависимостей
check_and_install_package "sshpass"
check_and_install_package "python3-wxgtk4.0"

echo "
Зависимости установлены
"

# Даём права на выполнение
chmod +x ./creator-n-u.sh ./mulses-1.2.py ./codename-mapping.py

# Путь к целевому файлу или директории
target="$HOME/mulsess-1.2/mulsess-1.2.py"  # Укажите полный путь к целевому файлу или директории

# Путь к папке рабочего стола пользователя
desktop="$HOME/Desktop"

# Имя для симлинка
linkName="$desktop/mulsess"  # Укажите имя симлинка

# Создание симлинка
if [ ! -e "$linkName" ]; then
    ln -s "$target" "$linkName"
    echo "Ярлык создан: $linkName -> $target"
else
    echo "Ярлык уже существует: $linkName"
fi

