from . import main


def run():
    return main.run()


def process_words(df, column_name):
    return main.process_words_from_dataframe(df, column_name)
