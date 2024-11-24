import pickle
import pandas as pd
import regex as re
from collections import Counter


def run():
    v = pickle.load(open("../inputs/output_2024-11-24_10-28-54.pkl", "rb"))
    df = pd.DataFrame(v)

    flattened_data = pd.concat(
        [df.drop(["fields"], axis=1), pd.json_normalize(df["fields"])], axis=1
    )

    return flattened_data


def process_words_from_dataframe(df):
    """
    Processes the words in a DataFrame to count kanji occurrences
    and map them to their originating metadata.

    Args:
        df (pd.DataFrame): The input DataFrame with columns like 'Word', 'id', 'Transliteration', 'Meaning'.

    Returns:
        kanji_counter (Counter): Counts of kanji occurrences.
        kanji_tree (dict): Mapping of kanji to metadata from the original DataFrame.
    """
    # Define regex pattern to match only kanji
    kanji_pattern = re.compile(r"\p{Script=Han}")

    kanji_counter = Counter()  # To count kanji occurrences
    kanji_tree = {}  # To map kanji to their originating rows

    # Iterate through rows in the DataFrame
    for _, row in df.dropna(subset=["Word"]).iterrows():
        word = row["Word"]
        kanji_only = "".join(kanji_pattern.findall(word))  # Extract kanji

        for kanji in kanji_only:
            # Increment kanji count
            kanji_counter[kanji] += 1

            # Add metadata to the kanji_tree
            if kanji not in kanji_tree:
                kanji_tree[kanji] = []
            kanji_tree[kanji].append(row.to_dict())  # Store entire row as metadata

    return kanji_counter, kanji_tree
