from typing import TypedDict, Dict, Literal, List


class Card(TypedDict):
    id: str
    fields: Dict[Literal["Word", "Transliteration", "Meaning", "PoS", "WordAudio"], str]


Cards = List[Card]
