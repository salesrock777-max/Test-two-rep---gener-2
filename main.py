"""
Ядро генератора паролей / Password Generation Core

Русский:
Данный модуль реализует логику генерации паролей и не имеет собственного интерфейса.
Предназначен для импорта и использования в других модулях, отвечающих за взаимодействие с пользователем. (консоль)
Поддерживает прямой запуск для отладки.

English:
This module implements password generation logic and has no user interface of its own.
Designed to be imported and used by other modules handling user interaction. (console)
Supports direct execution for debugging purposes.

Классы / Classes:

Choice_Initializer — обработка выбора символов / character selection processing

Generator — генерация паролей / password generation
"""

import string, secrets
from exceptioncode import EmptyChoiceError


"""DATA"""
lowercase = string.ascii_lowercase
uppercase = string.ascii_uppercase
digits = string.digits
punctuation = string.punctuation

select_true = ["yes", "1", "true", "y", "да", "д"]

class Choice_Initializer:
    """
    Initializes the selection of characters for password generation.

    This class handles the user's selection of character types and prepares the character set for generation.

    Attributes:
        _length (int): Password length
        _options_list (str): String with all selected characters
        _personal (str): String with personal characters (unique)
        _choice_digits (bool): Flag for using digits
        _choice_lowercase (bool): Flag for using lowercase letters
        _choice_uppercase (bool): Flag for using uppercase letters
        _choice_punctuation (bool): Flag for using special characters
        _choice_uniqueness (bool): Flag for character uniqueness
        _choice_personal (bool): Flag for using personal characters

    """

    def __init__(self, length, choice_digits, choice_lowercase, choice_uppercase, choice_punctuation, choice_uniqueness, choice_personal, personal):
        """
        Initializes a Choice_Initializer object.

        Args:
            length (int): Desired password length
            choice_digits (str): Select digits ("yes"/"no")
            choice_lowercase (str): Select lowercase letters
            choice_uppercase (str): Select uppercase letters
            choice_punctuation (str): Select special characters
            choice_uniqueness (str): Select uniqueness
            choice_personal (str): Select personal characters
            personal (str): String with personal characters, duplicates will be removed.

            Note:
            All choice_* parameters accept values ​​from select_true
            for True and any other values ​​for False.
        """

        self._length = length
        self._options_list = ""
        self._personal = ''.join(set(personal))

        self._choice_digits = self._processing_choice_digits(choice_digits)
        self._choice_lowercase = self._processing_choice_lowercase(choice_lowercase)
        self._choice_uppercase = self._processing_choice_uppercase(choice_uppercase)
        self._choice_punctuation = self._processing_choice_punctuation(choice_punctuation)
        self._choice_uniqueness = self._processing_choice_uniqueness(choice_uniqueness)
        self._choice_personal = self._processing_choice_personal(choice_personal)


    """
    The following block of methods is responsible for initializing the user's choice
    for each data type and converting the user input to a Boolean value.
    """
    def _processing_choice_digits(self, choice_digits):
        if choice_digits in select_true:
            self._options_list += digits
            return True
        else: return False
    def _processing_choice_lowercase(self, choice_lowercase):
        if choice_lowercase in select_true:
            self._options_list += lowercase
            return True
        else: return False
    def _processing_choice_uppercase(self, choice_uppercase):
        if choice_uppercase in select_true:
            self._options_list += uppercase
            return True
        else: return False
    def _processing_choice_punctuation(self, choice_punctuation):
        if choice_punctuation in select_true:
            self._options_list += punctuation
            return True
        else: return False
    def _processing_choice_uniqueness(self, choice_uniqueness):
        if choice_uniqueness in select_true:
            return True
        else: return False
    def _processing_choice_personal(self, choice_personal):
        if choice_personal in select_true:
            return True
        else: return False


    def _check_selection(self):
        """
        Checks whether at least one character type is selected.

        Returns:
            bool: True if at least one type is selected

        Raises:
            EmptyChoiceError: If no type is selected
        """

        if self._choice_digits or self._choice_lowercase or self._choice_uppercase or self._choice_punctuation:
            return True
        else:
            raise EmptyChoiceError("Вы выключили все параметры пароля!")

    def _check_personal(self):
        """
        Checks whether at least one character was passed.

        Returns:
            bool: True if at least one character was passed.

        Raise:
            EmptyChoiceError: if no characters were passed.
        """

        if self._personal:
            return True
        else:
            raise EmptyChoiceError("НЕльзя создать пароль без символов!")


class Generator(Choice_Initializer):
    """
    Generates passwords based on selected parameters.

    Inherits Choice_Initializer and adds the generator() method.

    Examples:
        >>> gen = Generator(10, "yes", "yes", "no", "no", "yes", "no", "")
        >>> password = gen.generator()
        >>> print(password)
        'a7k2m9p1q4'
    """
    def __init__(self, length, choice_digits, choice_lowercase, choice_uppercase, choice_punctuation, choice_uniqueness, choice_personal, personal):
        super().__init__(length, choice_digits, choice_lowercase, choice_uppercase, choice_punctuation, choice_uniqueness, choice_personal, personal)

    def generator(self):
        """
        Generates a password according to the selected parameters.

        Returns:
            str: Generated password

        Raises:
            EmptyChoiceError: If:
            - No character type selected
            - Unable to generate a unique password of the required length
            - Personal characters are empty when selected

        Notes:
            - If choice_personal is selected, only personal characters are used
            - If choice_uniqueness is selected, all characters in the password will be unique
            - For uniqueness, secrets.SystemRandom().sample() is used
            - For standard generation, secrets.choice() is used
        """

        if self._choice_personal:
            if self._choice_uniqueness and self._length <= len(self._personal):
                passwd = ''.join(secrets.SystemRandom().sample(self._personal, self._length))
                return passwd
            elif self._choice_uniqueness and self._length > len(self._personal):
                raise EmptyChoiceError("Невозможно создать уникальный пароль такой длины, с выбранными значениями!")
            elif self._check_personal():
                passwd = ''.join(secrets.choice(self._personal) for _ in range(self._length))
                return passwd


        elif self._choice_uniqueness and self._length <= len(self._options_list):
            passwd = ''.join(secrets.SystemRandom().sample(self._options_list, self._length))
            return passwd
        elif self._choice_uniqueness and self._length > len(self._options_list):
            raise EmptyChoiceError("Невозможно создать уникальный пароль такой длины, с выбранными значениями!")

        elif self._check_selection():
            passwd = ''.join(secrets.choice(self._options_list) for _ in range(self._length))
            return passwd


"""debugging"""
if __name__ == "__main__":
    # Для тестов напрямую из файла
    try:
        gen = Generator(10, "no", "no", "no", "no", "yes", "yes", "1234567890")
        print(gen.generator())
    except EmptyChoiceError as e:
        print(f"Error: {e}")
