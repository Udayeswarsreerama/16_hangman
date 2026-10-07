import random
from words import WORDS, HINTS
from stats import SessionStats


DIFFICULTIES = {
    "easy": {
        "lives": 8,
        "points": 3,
        "hint_cost": 1
    },
    "medium": {
        "lives": 6,
        "points": 5,
        "hint_cost": 1
    },
    "hard": {
        "lives": 4,
        "points": 7,
        "hint_cost": 1
    }
}


class HangmanGame:
    def __init__(self):
        self.score = 0
        self.streak = 0
        self.category = "technology"
        self.difficulty = "medium"
        self.secret = ""
        self.guessed = set()
        self.wrong = set()
        self.lives = 6
        self.hint_used = False
        self.stats = SessionStats()

    def start_round(self):
        self.secret = random.choice(WORDS[self.category])
        self.guessed.clear()
        self.wrong.clear()
        self.lives = DIFFICULTIES[self.difficulty]["lives"]
        self.hint_used = False

    def masked(self):
        return " ".join(
            ch if ch in self.guessed else "_"
            for ch in self.secret
        )

    def won(self):
        return all(
            ch in self.guessed
            for ch in set(self.secret)
        )

    def guess(self, letter):
        if len(letter) != 1 or not letter.isalpha():
            return "Enter one letter."

        # Task 1: repeated correct or incorrect guesses
        # must not affect the round again.
        if letter in self.guessed or letter in self.wrong:
            return "Already guessed."

        if letter in self.secret:
            self.guessed.add(letter)
            return "Correct."

        self.wrong.add(letter)
        self.lives -= 1
        return "Wrong."

    def use_hint(self):
        if self.hint_used:
            return None

        self.hint_used = True

        # Task 3: hint has a scoring penalty.
        hint_cost = DIFFICULTIES[self.difficulty]["hint_cost"]
        self.score = max(0, self.score - hint_cost)

        return HINTS.get(
            self.secret,
            "No hint available."
        )

    def play_round(self):
        self.start_round()

        while self.lives > 0 and not self.won():
            print("\nWord:", self.masked())
            print(
                "Wrong:",
                " ".join(sorted(self.wrong)) or "-"
            )
            print(
                "Lives:",
                self.lives,
                "Score:",
                self.score,
                "Streak:",
                self.streak
            )

            raw = input(
                "Letter, /hint, or /quit: "
            ).strip().lower()

            if raw == "/quit":
                return False

            if raw == "/hint":
                hint = self.use_hint()
                print(
                    hint
                    if hint
                    else "Hint already used."
                )
                continue

            print(self.guess(raw))

        if self.won():
            self.streak += 1

            # Task 3: difficulty changes the base score.
            base_points = DIFFICULTIES[
                self.difficulty
            ]["points"]

            self.score += base_points + self.streak

            # Task 2: record the completed round.
            self.stats.record(
                True,
                self.streak
            )

            print("Solved:", self.secret)
            return True

        # Lost round.
        self.streak = 0

        # Task 2: record the lost round.
        self.stats.record(
            False,
            self.streak
        )

        print(
            "Out of lives. The word was:",
            self.secret
        )

        return True

    def run(self):
        print("Hangman Challenge")
        print("A session consists of multiple rounds.")

        while True:
            # Task 3: choose difficulty.
            print(
                "\nDifficulties:",
                ", ".join(DIFFICULTIES)
            )

            difficulty = input(
                "Choose difficulty or q: "
            ).strip().lower()

            if difficulty == "q":
                return

            if difficulty not in DIFFICULTIES:
                print("Unknown difficulty.")
                continue

            self.difficulty = difficulty

            # Existing category selection.
            print(
                "\nCategories:",
                ", ".join(WORDS)
            )

            raw = input(
                "Choose category or q: "
            ).strip().lower()

            if raw == "q":
                return

            if raw not in WORDS:
                print("Unknown category.")
                continue

            self.category = raw

            if not self.play_round():
                return

            again = input(
                "Another round? [y/n]: "
            ).strip().lower()

            if again != "y":
                print(
                    "Final score:",
                    self.score
                )
                print(
                    "Rounds played:",
                    self.stats.rounds
                )
                print(
                    "Rounds won:",
                    self.stats.wins
                )
                print(
                    "Best streak:",
                    self.stats.best_streak
                )
                return
