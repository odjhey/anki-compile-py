import pickle
import requests

# AnkiConnect settings
ANKI_CONNECT_URL = "http://localhost:8765"
DECK_NAME = "zekanji"
MODEL_NAME = "zekanji"  # Use your note type name


def get_kanji_map():
    kanji_map = pickle.load(open("inputs/kanji_map.pkl", "rb"))

    print(list(kanji_map))
    # convert all to list
    return list(kanji_map.values())

    # # kanji_map is a dictionary, where kanji char is key, get first 2 kanji
    # first_2_keys = list(kanji_map.keys())[:2]
    # # get the value of the first key
    # first_item = kanji_map[first_2_keys[0]]
    # return [first_item]


def upload_as_anki_note(kanji, canonical, words):
    """Add a kanji note to Anki."""
    words_string = "<br/>".join(words)

    # Construct the note
    note = {
        "deckName": DECK_NAME,
        "modelName": MODEL_NAME,
        "fields": {"Kanji": kanji, "Words": words_string, "CanonicalId": canonical},
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
