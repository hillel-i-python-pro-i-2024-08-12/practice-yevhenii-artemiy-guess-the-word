from spellchecker import SpellChecker
import os

class WordGame:
   def __init__(self, excluded_letters=None, save_file='word_history.txt'):
       self.word_history = set()  # Використовуємо set для швидкого пошуку
       self.excluded_letters = excluded_letters if excluded_letters else ['ь', 'й', 'ы']  # Виключені літери
       self.last_letter = None  # Остання літера попереднього слова
       self.save_file = save_file  # Ім'я файлу для збереження історії

       self.spell = SpellChecker(language=None)  # Ініціалізуємо перевірку правопису
       self.spell.word_frequency.load_text_file('100000-russian-words.txt')

       self.load_history_from_file()


   def normalize_word(self, word):
       word = word.strip().lower()  # Відсікаємо зайві символи і приводимо до нижнього регістру
       return word


   def check_spelling(self, word):
       # Перевіряємо чи є слово правильним
        is_correct = self.spell[word]
        return is_correct, word if is_correct else self.spell.correction(word)


   def get_last_valid_letter(self, word):
       # Отримуємо останню "валідну" літеру слова (не з excluded_letters)
       for letter in reversed(word):
           if letter not in self.excluded_letters:
               return letter
       return None


   def add_word(self, word):
       word = self.normalize_word(word)


       # Перевірка правопису слова
       is_valid, corrected_word = self.check_spelling(word)
       if not is_valid:
           return f"Слово '{word}' невірне. Можливо, ви мали на увазі: '{corrected_word}'?"


       if word in self.word_history:
           return f"Слово '{word}' вже було використано."


       if self.last_letter and word[0] != self.last_letter:
           return f"Слово повинно починатися з літери '{self.last_letter.upper()}'."


       self.word_history.add(word)
       self.last_letter = self.get_last_valid_letter(word)


       # Зберігаємо слово у файл
       self.save_word_to_file(word)


       return f"Слово '{word}' додано. Тепер наступне слово повинно починатися з літери '{self.last_letter.upper()}'."


   def save_word_to_file(self, word):
       with open(self.save_file, 'a', encoding='utf-8') as file:
           file.write(word + '\n')


   def load_history_from_file(self):
       if os.path.exists(self.save_file):
           with open(self.save_file, 'r', encoding='utf-8') as file:
               for line in file:
                   word = line.strip()
                   self.word_history.add(word)
                   self.last_letter = self.get_last_valid_letter(word)
           print(f"Історія слів завантажена з файлу: {self.save_file}")
           print(f"Останнє слово: {word}")
       else:
           print("Файл з історією не знайдено, починаємо нову гру.")


def main():
   game = WordGame(save_file='word_history.txt')


   while True:
        word = input("Введіть слово: ")
        if word.lower() == 'вихід':
            print("Гру завершено.")
            break
        result = game.add_word(word)
        print(result)


if __name__ == "__main__":
   main()