import random


TARGET_PHRASE = "METHINKS IT IS LIKE A WEASEL"
POPULATION_SIZE = 100
MUTATION_RATE = 0.05
CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "


def random_character() -> str:
    return random.choice(CHARACTERS)


def random_phrase(length: int) -> str:
    """Generate a random phrase with the same length as the target phrase."""
    return ''.join(random_character() for _ in range(length))


def mutate(phrase: str) -> str:
    """Apply mutations to each character of the phrase, with a 5% chance."""
    return ''.join(
        random_character() if random.random() < MUTATION_RATE else c
        for c in phrase
    )


def score(phrase: str) -> int:
    """Score the phrase by comparing it to the target phrase."""
    return sum(1 for a, b in zip(phrase, TARGET_PHRASE) if a == b)


def main() -> None:
    """Run the Weasel Program algorithm."""
    phrase = random_phrase(len(TARGET_PHRASE))
    generation = 0

    while True:
        generation += 1
        population = [mutate(phrase) for _ in range(POPULATION_SIZE)]
        scores = [score(p) for p in population]

        best_score = max(scores)
        best_phrase = population[scores.index(best_score)]

        print(f"Generation {generation}: {best_phrase} (Score: {best_score})")

        if best_score == len(TARGET_PHRASE):
            print(f"Target phrase found in {generation} generations!")
            break

        phrase = best_phrase


if __name__ == "__main__":
    main()
