import pickle
import requests
import json

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


def update_anki_note(note_id, kanji, canonical, words_meta_json):
    """Update an existing Anki note."""
    response = requests.post(
        ANKI_CONNECT_URL,
        json={
            "action": "updateNoteFields",
            "version": 6,
            "params": {
                "note": {
                    "id": note_id,
                    "fields": {
                        "Kanji": kanji,
                        "CanonicalId": canonical,
                        "richInfo": words_meta_json,
                    },
                },
            },
        },
    )

    if response.status_code == 200:
        result = response.json()
        if "error" in result and result["error"]:
            print(f"Error updating note for {kanji}: {result['error']}")
        else:
            print(f"Note for {kanji} updated successfully!")
    else:
        print(f"Failed to connect to AnkiConnect for updating {kanji}")


def add_anki_note(kanji, canonical, words_meta_json):
    """Add a new Anki note."""
    note = {
        "deckName": DECK_NAME,
        "modelName": MODEL_NAME,
        "fields": {
            "Kanji": kanji,
            "CanonicalId": canonical,
            "richInfo": words_meta_json,
        },
    }

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
        print(f"Failed to connect to AnkiConnect for adding {kanji}")


def upload_as_anki_note(kanji, canonical, wordsMeta):
    """Add or update a kanji note in Anki."""
    words_meta_json = json.dumps(wordsMeta)

    # Find existing notes with the same Kanji or CanonicalId
    query = f"deck:{DECK_NAME} note:{MODEL_NAME} (Kanji:{kanji} AND CanonicalId:{canonical})"
    response = requests.post(
        ANKI_CONNECT_URL,
        json={
            "action": "findNotes",
            "version": 6,
            "params": {
                "query": query,
            },
        },
    )

    if response.status_code == 200:
        result = response.json()
        existing_notes = result.get("result", [])
    else:
        print(f"Failed to query existing notes for {kanji}")
        return

    if existing_notes:
        # Update the first matching note
        note_id = existing_notes[0]  # Assuming one match
        update_anki_note(note_id, kanji, canonical, words_meta_json)
    else:
        # Add a new note
        add_anki_note(kanji, canonical, words_meta_json)
