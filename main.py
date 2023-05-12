import re


class Decoder:
    alph = 'абвгдеёжзийклмнопрстуфчцчшщъыьэюяңөү'

    def __init__(self, stats_text, input_text):
        self.stats_text = stats_text
        self.input_text = input_text

        self.stats_frequency, most_often_stat_letter = Decoder.calculate_frequency_of_letters(stats_text)
        self.input_frequency, most_often_input_letter = Decoder.calculate_frequency_of_letters(input_text)

        self.stats_words = Decoder.split_on_words(stats_text)
        self.input_words = Decoder.split_on_words(input_text)

        self.key = dict()

        for k in self.input_frequency:
            self.key[k[0]] = None

        self.key[most_often_input_letter] = most_often_stat_letter

    def unknown_letters(self):
        return ''.join((c for c in self.alph if c not in self.key.values()))

    def is_need_to_check(self, word: str):
        for k in self.key:
            if self.key[k] is not None and k in word:
                return True
        return False

    def calculate(self):
        while True:
            print(self.key)
            examples = []

            for word in self.input_words:
                # print(word)
                if self.is_need_to_check(word):
                    reg = ''

                    for s in word:
                        if self.key.get(s, None) is None:
                            reg += f'[{self.unknown_letters()}]'
                        else:
                            reg += self.key[s]

                    reg += '$'

                    matches = list(filter(lambda w: re.match(reg, w), self.stats_words))
                    matches = list(filter(lambda x: Decoder.validate(x, word), matches))

                    # print(word, reg, len(matches))

                    if len(matches) == 1 and any(map(lambda s: s not in self.key.values(), matches[0])):
                        # print(matches[0], word)
                        err = 0.0
                        is_valid = True

                        for i in range(len(matches[0])):
                            if self.key.get(word[i]) is None:
                                err += abs(
                                    self.input_frequency.get(word[i], 10000000000) * 1.0 / self.stats_frequency.get(matches[0][i], 0.0001) - 1)

                                if matches[0][i] in list(self.key.values()):
                                    is_valid = False
                                    break

                        if is_valid:
                            examples.append((word, matches[0], err / len(word)))

            if len(examples) == 0:
                break

            examples.sort(key=lambda x: x[2])
            changed = True

            for example in examples[:8]:
                for i in range(len(example[0])):
                    if self.key.get(example[0][i], "1") is None and example[1][i] not in self.key.values():
                        changed = False
                        self.key[example[0][i]] = example[1][i]
                print(example)

            if changed:
                break

    def show_result(self):
        text = ''

        for w in self.input_text:
            if w.isalpha():
                upp = w != w.lower()
                w = w.lower()
                text += (self.key[w] if not upp else self.key[w].upper()) if self.key.get(w, None) is not None else '-'
            else:
                text += w

        print(text)

    def validate_key(self):
        for v in self.key.values():
            keys = []
            for k in self.key.keys():
                if self.key[k] == v:
                    keys.append(k)

            if len(keys) > 1:
                print("Key collide!")

                for k in keys:
                    print(f"{k}: {v}")

                print(f"Not used yet: {self.unknown_letters()}")
                return False
        return True

    def change_key(self):
        while True:
            print(self.key)
            value = input("New key (а:я): ").lower()

            self.validate_key()

            if value == "q":
                break

            if len(value) != 3 and value[0] not in self.key.keys():
                print("Input error")
                continue

            for k in self.key.keys():
                if k != value[0] and self.key[k] == value[-1] and self.key[value[0]] is not None:
                    self.key[k] = self.key[value[0]]

            self.key[value[0]] = value[-1]


    @staticmethod
    def calculate_frequency_of_letters(text):
        alph = 'абвгдеёжзийклмнопрстуфчцчшщъыьэюяңөү'
        text = text.lower()
        d = dict()
        tot = 0
        for c in text:
            if c in alph:
                d[c] = d.get(c, 0) + 1
                tot += 1

        for k in d:
            d[k] /= tot * 0.01

        si = list(d.items())
        si.sort(key=lambda x: -x[1])

        return dict(si), si[0][0]

    @staticmethod
    def split_on_words(text: str):
        text = re.sub(r'[^\w\s]', '', text.lower())
        text = text.lower()
        return set([word for word in text.split() if word.isalpha()])

    @staticmethod
    def validate(word: str, other_word: str) -> bool:
        if len(word) != len(other_word):
            return False
        for i in range(len(word)):
            for j in range(i, len(word)):
                if not (word[i] == word[j]) == (other_word[i] == other_word[j]):
                    return False
        return True


encoded_text = open('input.txt', 'r', encoding='UTF-8').read()
sample_text = open('sample_text.txt', 'r', encoding='UTF-8').read().replace('www.bizdin.kg', '')

decoder = Decoder(sample_text, encoded_text)

print(decoder.stats_frequency)
print(decoder.input_frequency)

decoder.calculate()
decoder.show_result()

decoder.change_key()
decoder.show_result()
