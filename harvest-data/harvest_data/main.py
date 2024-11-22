import datetime
from .extract_from_api import get_all_cards, save_to_text


def run():
    print("Hello, world!")

    cards = get_all_cards("aaa_dailies::vocabs")

    # Generate timestamp in 'YYYY-MM-DD_HH-MM-SS' format
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # add date and time to filename
    save_to_text(cards, f"output/output_{timestamp}.txt")
