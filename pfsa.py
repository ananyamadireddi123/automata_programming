import argparse
import pytest
import json

from collections import defaultdict


def construct(file_str: str) -> dict[str, dict[str, float]]:
    # Initialize an empty result dictionary
    pfsa = {"*": {}}

    # Split the input text into words
    words = file_str.split()

    for word in words:

        word = word.lower()
        l_words = word.lower()

        if '*' not in pfsa:
            pfsa['*'] = {}
        temp = word+'*'

        start = "*"  # Initialize the state for each word
        for letter in l_words:

            if start not in pfsa:
                pfsa[start] = {}

            if start != '*':
                complete += letter
            else:
                complete = letter

            if complete not in pfsa[start]:
                pfsa[start][complete] = 0

            pfsa[start][complete] += 1
            start = complete  # Update the state by appending the character
            
        if word not in pfsa:
            pfsa[word] = {}
        pfsa[word][temp] = 1    

    # Normalize transition probabilities
    for state, transitions in pfsa.items():
        total_probability = sum(transitions.values())
        for char, count in transitions.items():
            pfsa[state][char] /= total_probability

    return pfsa


def main():
    """
    The command for running is `python pfsa.py text.txt`. This will generate
    a file `text.json` which you will be using for generation.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="xxx")
    args = parser.parse_args()

    with open(args.file, "r") as file:
        contents = file.read()
        output = construct(contents)

    name = args.file.split(".")[0]

    with open(f"{name}.json", "w") as file:
        json.dump(output, file)


if __name__ == "__main__":
    main()


STRINGS = ["A cat", "A CAT", "", "A", "A A A A"]
DICTIONARIES = [
    {
        "*": {"a": 0.5, "c": 0.5},
        "a": {"a*": 1.0},
        "c": {"ca": 1.0},
        "ca": {"cat": 1.0},
        "cat": {"cat*": 1.0},
    },
    {
        "*": {"a": 0.5, "c": 0.5},
        "a": {"a*": 1.0},
        "c": {"ca": 1.0},
        "ca": {"cat": 1.0},
        "cat": {"cat*": 1.0},
    },
    {
        "*": {},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
]


@pytest.mark.parametrize("string, pfsa", list(zip(STRINGS, DICTIONARIES)))
def test_output_match(string, pfsa):
    """
    To test, install `pytest` beforehand in your Python environment.

    Run `pytest pfsa.py` Your code must pass all tests. There are additional
    hidden tests that your code will be tested on during VIVA.

    """

    result = construct(string)
    # print(result)

    rounded_result = {state: {char: round(prob, 5) for char, prob in transitions.items(
    )} for state, transitions in result.items()}
    rounded_pfsa = {state: {char: round(prob, 5) for char, prob in transitions.items(
    )} for state, transitions in pfsa.items()}

    assert rounded_result == rounded_pfsa
    # assert result == pfsa
