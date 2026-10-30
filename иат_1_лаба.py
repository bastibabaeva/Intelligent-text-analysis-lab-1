
import pymorphy3
import nltk

from nltk.tokenize import sent_tokenize, word_tokenize

# Морфологический анализатор
morph = pymorphy3.MorphAnalyzer()

# Загружаем необходимые данные NLTK
nltk.download("punkt")
nltk.download("punkt_tab")

with open("text.txt", "r", encoding="utf-8") as file:
    text = file.read()

print(text)

# СЕГМЕНТАЦИЯ:
# разбиваем текст на предложения
sentences = sent_tokenize(text, language="russian")

print("Количество предложений:", len(sentences))

# Обрабатываем каждое предложение
for sentence in sentences:

    # ТОКЕНИЗАЦИЯ:
    # разбиваем предложение на отдельные слова и знаки препинания
    tokens = word_tokenize(sentence, language="russian")

    words = []

    # МОРФОЛОГИЧЕСКИЙ АНАЛИЗ
    for token in tokens:

        # Пропускаем знаки препинания, то есть если в токене нет ни одной буквы, то пропускаем
        if not any(char.isalpha() for char in token):
            continue

        parsed = morph.parse(token)[0]

        words.append({
            "word": token,
            "lemma": parsed.normal_form, #нач форма слова
            "pos": parsed.tag.POS,    #часть речи
            "gender": parsed.tag.gender,  #род
            "number": parsed.tag.number,   #число
            "case": parsed.tag.case,     #падеж
            "is_pronoun": "Apro" in parsed.tag #есть ли местоименное прилагательное в теге
        })

    # Ищем пары соседних слов
    for i in range(len(words) - 1):

        word1 = words[i]
        word2 = words[i + 1]


        # Первое слово - это сущ, прилаг или краткое прилаг?
        word_one = word1["pos"] in ("NOUN", "ADJF", "ADJS")

        # Второе слово - это сущ, прилаг или краткое прилаг?
        word_two = word2["pos"] in ("NOUN", "ADJF", "ADJS")


        # Если оба слова не сущ или прилаг, то пропускаем
        if not (word_one and word_two):
            continue

        # Если одно из двух соседних слов местоимение то пропускаем
        if word1["is_pronoun"] or word2["is_pronoun"]:
            continue

        # Проверяем наличие рода, числа и падежа
        if (
            word1["gender"] is not None and
            word2["gender"] is not None and #род
            word1["number"] is not None and
            word2["number"] is not None and # число
            word1["case"] is not None and
            word2["case"] is not None     #падеж
        ):

            # Проверяем совпадение рода, числа и падежа
            if (
                word1["gender"] == word2["gender"] and
                word1["number"] == word2["number"] and
                word1["case"] == word2["case"]
            ):

                # Выводим леммы
                print(word1["lemma"], word2["lemma"])
