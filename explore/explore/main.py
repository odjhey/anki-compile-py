import pickle
import pandas as pd
import regex as re
from collections import Counter


def run():
    v = pickle.load(open("../inputs/output_2024-11-23_13-05-57.pkl", "rb"))
    df = pd.DataFrame(v)

    flattened_data = pd.concat(
        [df.drop(["fields"], axis=1), pd.json_normalize(df["fields"])], axis=1
    )

    return flattened_data


def process_words_from_dataframe(df, column_name):
    # Define regex pattern to match only kanji
    kanji_pattern = re.compile(r"\p{Script=Han}")

    kanji_counter = Counter()  # To count kanji occurrences
    kanji_tree = {}  # To map kanji to their originating words

    # Iterate through the column
    for word in df[column_name].dropna():
        # Remove kana and other non-kanji characters
        kanji_only = "".join(kanji_pattern.findall(word))

        # Count kanji
        for kanji in kanji_only:
            kanji_counter[kanji] += 1
            kanji_tree.setdefault(kanji, set()).add(word)

    return kanji_counter, kanji_tree
