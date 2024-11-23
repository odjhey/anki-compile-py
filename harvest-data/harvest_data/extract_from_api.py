import requests
import pickle

ANKI_CONNECT_URL = "http://localhost:8765"


def invoke(action, **params):
    """Send a JSON-RPC request to AnkiConnect."""
    response = requests.post(
        ANKI_CONNECT_URL, json={"action": action, "version": 6, "params": params}
    )
    response.raise_for_status()
    return response.json()["result"]


def get_all_cards(deck_name):
    """Fetch all cards from the specified deck."""
    note_ids = invoke("findNotes", query=f"deck:{deck_name}")
    notes = invoke("notesInfo", notes=note_ids)
    desired_fields = {"Word", "Transliteration", "Meaning", "Part of Speech"}

    return [
        {
            "id": note["noteId"],
            "fields": {
                ("PoS" if key == "Part of Speech" else key): field["value"]
                for key, field in note["fields"].items()
                if key in desired_fields
            },
        }
        for note in notes
    ]


def save_to_text(cards, file_path):
    with open(file_path, "w") as file:
        for card in cards:
            file.write(f"Card ID: {card['id']}\n")
            for field_name, field_value in card["fields"].items():
                file.write(f"  {field_name}: {field_value}\n")
            file.write("\n")
    print(f"Data has been saved to: {file_path}")


def save_to_pickle(data, file_path):
    """
    Save data to a file using pickle.

    Args:
        data: The Python object to pickle (e.g., list, dict).
        file_path: The file path where the data will be saved (e.g., 'output/data.pkl').
    """
    with open(file_path, "wb") as file:
        pickle.dump(data, file)
    print(f"Data has been saved to: {file_path}")
