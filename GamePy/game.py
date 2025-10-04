# game.py
# Здесь находится ВСЯ логика игры: загрузка слов, ввод, проверка, рисование виселицы и т.д.

import random

# Глобальные переменные (можно использовать внутри функций)
WORDS_FILE = "words.txt"  # имя файла со словами
MAX_ATTEMPTS = 6          # сколько частей у виселицы

def load_words():
    """
    Читает слова и подсказки из файла words.txt.
    Возвращает список кортежей: [('слово', 'подсказка'), ...]
    """
    words = []
    try:
        with open(WORDS_FILE, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line and " - " in line:
                    word, hint = line.split(" - ", 1)
                    words.append((word.strip().lower(), hint.strip()))
    except FileNotFoundError:
        print(f"Файл {WORDS_FILE} не найден! Создайте его.")
        return [("тест", "пример слова")]
    return words

def get_random_word():
    """
    Выбирает случайное слово и подсказку из списка.
    """
    words = load_words()
    return random.choice(words)

def display_hangman(attempts):
    """
    Возвращает рисунок виселицы в зависимости от количества ошибок (attempts).
    attempts: сколько ошибок уже сделано (от 0 до MAX_ATTEMPTS)
    """
    stages = [
        """
           --------
           |      |
           |      
           |    
           |      
           |     
        =========
        """,
        """
           --------
           |      |
           |      O
           |    
           |      
           |     
        =========
        """,
        """
           --------
           |      |
           |      O
           |      |
           |      
           |     
        =========
        """,
        """
           --------
           |      |
           |      O
           |     /|
           |      
           |     
        =========
        """,
        """
           --------
           |      |
           |      O
           |     /|\\
           |      
           |     
        =========
        """,
        """
           --------
           |      |
           |      O
           |     /|\\
           |     /
           |     
        =========
        """,
        """
           --------
           |      |
           |      O
           |     /|\\
           |     / \\
           |     
        =========
        """
    ]
    # Возвращаем нужный этап (но не выходим за границы)
    return stages[min(attempts, len(stages) - 1)]

def play():
    """
    Основная функция игры.
    """
    print("🎮 Добро пожаловать в игру 'Виселица на поле чудес'!")
    
    # Загадываем слово и подсказку
    secret_word, hint = get_random_word()
    guessed_letters = []          # буквы, которые игрок уже назвал
    correct_letters = []          # правильно угаданные буквы
    attempts = 0                  # количество ошибок

    print(f"\nПодсказка: {hint}")
    print("Слово загадано. У вас есть 6 попыток!")

    while attempts < MAX_ATTEMPTS:
        # Показываем текущее состояние слова (например: _ _ т)
        display_word = ""
        for letter in secret_word:
            if letter in correct_letters:
                display_word += letter + " "
            else:
                display_word += "_ "
        print("\nСлово:", display_word.strip())

        # Показываем виселицу
        print(display_hangman(attempts))

        # Если слово угадано полностью
        if all(letter in correct_letters for letter in secret_word):
            print("\n🎉 Поздравляем! Вы угадали слово:", secret_word)
            return

        # Ввод буквы
        guess = input("Введите букву: ").strip().lower()

        # Проверка корректности ввода
        if len(guess) != 1 or not guess.isalpha():
            print("Пожалуйста, введите одну букву!")
            continue

        if guess in guessed_letters:
            print("Вы уже пробовали эту букву!")
            continue

        # Добавляем букву в список попыток
        guessed_letters.append(guess)

        # Проверяем, есть ли буква в слове
        if guess in secret_word:
            correct_letters.append(guess)
            print("✅ Верно!")
        else:
            attempts += 1
            print("❌ Неверно!")

    # Если закончились попытки
    print(display_hangman(attempts))
    print("\n💀 Вы проиграли! Загаданное слово было:", secret_word)