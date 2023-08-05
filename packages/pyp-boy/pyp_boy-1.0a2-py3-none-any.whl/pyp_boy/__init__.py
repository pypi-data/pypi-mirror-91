class PypBoy(object):
    # word_list = ["hello", "shell", "bells", "hells"]

    def __init__(self, word_list):
        self.word_list = word_list

        self.possibles = []
        # self.example_list = [
        #     "LOYALIST",
        #     "FEVERISH",
        #     "CITIZENS",
        #     "RESULTED",
        #     "SUDDENLY",
        #     "UNWANTED",
        #     "HUMANITY",
        #     "CONQUEST",
        #
        # ]

    def compare(self, guess_str, word, num_correct):
        correct = 0
        for x, y in zip(guess_str, word):
            print(f"Comparing {x} amd {y}")
            if x == y:
                print("Match!")
                correct += 1

        print(correct)

        if int(correct) == int(num_correct):
            correct = 0
            self.possibles.append(word)
            print(self.possibles)
            return True

    def guess(self, guess_str, num_correct):

        new_list = []
        print(guess_str)
        print(num_correct)

        for word in self.word_list:
            if word == guess_str:
                pass
            else:
                if self.compare(guess_str, word, num_correct):
                    self.possibles.append(word)

        self.word_list = self.possibles

        return self.word_list

    class Stats(object):
        def __init__(self):
            self.ledger = {}

        def add(self, guessed_word, ):
            entry = {}

    class CLI()
