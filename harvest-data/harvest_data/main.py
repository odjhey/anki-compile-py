import datetime
from .extract_from_api import get_all_cards, save_to_text, save_to_pickle
from .upload_to_anki import get_kanji_map, upload_as_anki_note


def run():
    print("Hello, world!")

    cards = get_all_cards("aaa_dailies::vocabs")

    # Generate timestamp in 'YYYY-MM-DD_HH-MM-SS' format
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # add date and time to filename
    save_to_text(cards, f"outputs/output_{timestamp}.txt")
    save_to_pickle(cards, f"outputs/output_{timestamp}.pkl")


def upload_to_anki():
    print("Uploading to Anki...")
    # [{'kanji': '起', 'canonical': '08d77', 'words': {'起こす', '起きる', '早起き', '起こる'}}]
    kanji_map = get_kanji_map()
    # upload all kanji_map
    for kanji in kanji_map:
        upload_as_anki_note(
            kanji.get("kanji"), kanji.get("canonical"), kanji.get("words")
        )
