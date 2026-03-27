#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Консольный интерфейс для генератора паролей / Console Interface for Password Generator

Русский:
    Данный модуль предоставляет интерфейс командной строки для взаимодействия
    с ядром генератора паролей (main.py). Позволяет пользователю задавать параметры
    генерации и получать пароли в консоли.

English:
    This module provides a command-line interface for interacting with the
    password generator core (main.py). Allows the user to set generation parameters
    and receive passwords in the console.

Использование / Usage:
    python cli.py

Зависимости / Dependencies:
    - main.py (ядро генератора / generator core)
    - exceptioncode.py (пользовательские исключения / custom exceptions)
"""


from main import Generator, select_true
from exceptioncode import EmptyChoiceError


def data_acquisition():
    """
    Collect user data and generate passwords.

    Prompts the user to enter generation parameters:
    - Password length
    - Number of passwords to generate
    - Use of personal characters (optional)
    - Character sets (numbers, letters, special characters)
    - Uniqueness mode

    Depending on the user's selection, creates instances of the Generator class
    and displays the generated passwords.

    Args:
    None

    Returns:
    None

    Raises:
    EmptyChoiceError: If no character type is selected (processed internally)
    """

    length = input("\nВведите в сколько символов хотите генерировать пароль? (от 3 до 30)\n")
    number_of_cycles = input("\nСколько паролей за раз вы хотите сгенерировать? (от 1 до 5)\n")

    try:
        length = int(length)
        if length < 3 or length > 30:
            raise ValueError
    except ValueError:
        print("Ошибка! Автоматически заменена на 12 символов.")
        length = 12
    except Exception as e:
        print(f"Ошибка: {e}")

    try:
        number_of_cycles = int(number_of_cycles)
        if number_of_cycles < 1 or number_of_cycles > 5:
            raise ValueError
    except ValueError:
        print("Ошибка! Установлено количество 5 паролей.")
        number_of_cycles = 5
    except Exception as e:
        print(f"Ошибка: {e}")


    choice_personal = input("Хотите ли вы генерировать пароль из своих значений?\n")
    if choice_personal in select_true:
        personal = input("Введите свои значения для пароля (будут приняты только уникальные!)\n")
        choice_uniqueness = input("Генерировать без повторений?\n")

        for _ in range(number_of_cycles):
            try:
                gen = Generator(length, "no", "no", "no", "no", choice_uniqueness, "yes", personal)
                print(gen.generator())
            except EmptyChoiceError as e:
                print(f"Error: {e}")

    else:
        choice_digits = input("Включать цифры в пароль?\n")
        choice_lowercase = input("Включать маленькие буквы в пароль?\n")
        choice_uppercase = input("Включать большие буквы в пароль?\n")
        choice_punctuation = input("Включать спец. символы в пароль?\n")
        choice_uniqueness = input("Генерировать без повторений?\n")

        for _ in range(number_of_cycles):
            try:
                gen = Generator(length, choice_digits, choice_lowercase, choice_uppercase, choice_punctuation, choice_uniqueness, "no", "")
                print(gen.generator())
            except EmptyChoiceError as e:
                print(f"Error: {e}")

def main():
    while True:
        greetings = input("Генератор паролей\nНажмите любую клавишу чтобы продолжить, чтобы закрыть программу введите 'stop'.\n")
        if greetings == 'stop':
            return 0

        data_acquisition()
main()
