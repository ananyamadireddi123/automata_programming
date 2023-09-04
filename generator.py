# import argparse
# import json
# import random

# def generate(pfsa: dict[str, dict[str, float]], word_count: int) -> str:
#     """Generates a string of `word_count` number of words based on the PFSA.

#     Args:
#         pfsa (dict): The PFSA representation of the language.
#         word_count (int): The number of words to generate.

#     Returns:
#         str: The generated string.
#     """
#     if not pfsa:
#         return ""

#     state = "*"
#     generated_words = []

#     for _ in range(word_count):
#         while True:
#             char = select_transition(pfsa[state])
#             if char == "":
#                 break
#             if char != '*':
#                 temp = char
#             state = char if char in pfsa else "*"

#             if state == "*":
#                 break

#         generated_words.append(temp)
#         state = "*"

#     return " ".join(generated_words)

# def select_transition(transitions):
#     if not transitions:
#         return ""

#     r = random.random()
#     cumulative_prob = 0.0
#     for char, prob in transitions.items():
#         cumulative_prob += prob
#         if r <= cumulative_prob:
#             return char
#     return ""
   
                            

# def main():
#     """
#     The command for running is `python generator.py text.json 5`. This will
#     generate a file `text_sample.txt` which has 5 randomly sampled words.
#     """
#     parser = argparse.ArgumentParser()
#     parser.add_argument("file", type=str, help="text.txt")
#     parser.add_argument("count", type=int, help="10")
#     args = parser.parse_args()

#     with open(args.file, "r") as file:
#         data = json.load(file)
#         output = generate(data, args.count)

#     name = args.file.split(".")[0]

#     with open(f"{name}_sample.txt", "w") as file:
#         file.write(output)

#     with open(f"{name}_sample.txt", "w") as file:
#         file.write(output)


# if __name__ == "__main__":
#     main()


# DICTIONARIES = [
#     {
#         "*": {"a": 1.0},
#         "a": {"a*": 1.0},
#     },
#     {
#         "*": {"a": 1.0},
#         "a": {"a*": 1.0},
#     },
#     {
#         "*": {"a": 1.0},
#         "a": {"a*": 1.0},
#     },
#     {
#         "*": {"c": 1.0},
#         "c": {"ca": 1.0},
#         "ca": {"cat": 1.0},
#         "cat": {"cat*": 1.0},
#     },
# ]
# STRINGS = [
#     "a",
#     "a a a a a",
#     "",
#     "cat cat cat cat",
# ]
# COUNT = [1, 5, 0, 4]

# COMBINED = [(d, s, c) for d, (s, c) in zip(DICTIONARIES, zip(STRINGS, COUNT))]

import argparse
import pytest
import json
import random

def select_transition(transitions):
        if not transitions:
            return ""
        
        r = random.random()
        cumulative_prob = 0.0
        for char, prob in transitions.items():
            cumulative_prob += prob
            if r <= cumulative_prob:
                return char
        return ""

def generate(pfsa: dict[str, dict[str, float]], word_count: int) -> str:
    """Takes in the PFSA and generates a string of `word_count` number of words."""
    if not pfsa:
        return ""

    state = "*"
    generated_words = []

    for _ in range(word_count): 
        while True:
            char = select_transition(pfsa[state])
            if char == "":
                break
            if char != '*':
                 
                temp=char
            state = char if char in pfsa else "*"

            if state == "*":
                break

        generated_words.append(temp)
        state = "*"

    return " ".join(generated_words)



def main():
    """
    The command for running is `python generator.py text.json 5`. This will
    generate a file `text_sample.txt` which has 5 randomly sampled words.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="text.txt")
    parser.add_argument("count", type=int, help="10")
    args = parser.parse_args()

    with open(args.file, "r") as file:
        data = json.load(file)
        output = generate(data, args.count)

    name = args.file.split(".")[0]

    with open(f"{name}_sample.txt", "w") as file:
        file.write(output)

    with open(f"{name}_sample.txt", "w") as file:
        file.write(output)


if __name__ == "__main__":
    main()


DICTIONARIES = [
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"c": 1.0},
        "c": {"ca": 1.0},
        "ca": {"cat": 1.0},
        "cat": {"cat*": 1.0},
    },
]
STRINGS = [
    "a",
    "a a a a a",
    "",
    "cat cat cat cat",
]
COUNT = [1, 5, 0, 4]

COMBINED = [(d, s, c) for d, (s, c) in zip(DICTIONARIES, zip(STRINGS, COUNT))]


@pytest.mark.parametrize("pfsa, string, count", COMBINED)
def test_output_match(pfsa, string, count):
    """
    To test, install `pytest` beforehand in your Python environment.

    Run `pytest pfsa.py` Your code must pass all tests. There are additional
    hidden tests that your code will be tested on during VIVA.
    """
    result = generate(pfsa, count)
    #assert result == string

 
