import pickle
import requests

# AnkiConnect settings
ANKI_CONNECT_URL = "http://localhost:8765"
DECK_NAME = "zekanji"
MODEL_NAME = "zekanji"  # Use your note type name


def get_kanji_map():
    kanji_map = pickle.load(open("inputs/kanji_map.pkl", "rb"))

    # convert all to list
    return list(kanji_map.values())

    # # kanji_map is a dictionary, where kanji char is key, get first 2 kanji
    # first_2_keys = list(kanji_map.keys())[:2]
    # # get the value of the first key
    # first_item = kanji_map[first_2_keys[0]]
    # return [first_item]


def upload_as_anki_note(kanji, canonical, wordsMeta):
    """Add a kanji note to Anki."""

    # words has format
    # [{'Word': '起こす', 'Transliteration': 'おこす', 'Meaning': 'wake (someone) up', 'PoS': 'Verb'},
    #  {'Word': '起きる', 'Transliteration': 'おきる', 'Meaning': 'occur, happen', 'PoS': 'Verb'},
    #  {'Word': '起きる', 'Transliteration': 'おきる', 'Meaning': 'get up, get out of bed', 'PoS': 'Verb'},
    #  {'Word': '起こる', 'Transliteration': 'おこる', 'Meaning': 'happen', 'PoS': 'Verb'},
    #  {'Word': '早起き', 'Transliteration': 'はやおき', 'Meaning': 'getting up early', 'PoS': 'Verbal Noun'}]

    words = [word["Word"] for word in wordsMeta]
    words_string = "<br/>".join(words)

    words_with_transliteration = [
        f"{ word['Word'] } ({word['Transliteration']}) - {word['Meaning']}"
        for word in wordsMeta
    ]

    words_with_transliteration_string = "<br/>".join(words_with_transliteration)

    # Construct the note
    note = {
        "deckName": DECK_NAME,
        "modelName": MODEL_NAME,
        "fields": {
            "Kanji": kanji,
            "Words": words_string,
            "CanonicalId": canonical,
            "WordsWithMeaning": words_with_transliteration_string,
        },
    }

    # Send request to AnkiConnect
    response = requests.post(
        ANKI_CONNECT_URL,
        json={"action": "addNote", "version": 6, "params": {"note": note}},
    )
    if response.status_code == 200:
        result = response.json()
        if "error" in result and result["error"]:
            print(f"Error adding note for {kanji}: {result['error']}")
        else:
            print(f"Note for {kanji} added successfully!")
    else:
        print(f"Failed to connect to AnkiConnect for {kanji}")
