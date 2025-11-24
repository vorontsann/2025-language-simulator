class DataManager:
    def load_words_from_csv(self, path):
        raise NotImplementedError()

    def get_topics(self, language_code):
        raise NotImplementedError()

    def save_progress(self, progress):
        raise NotImplementedError()

    def load_progress(self, user_id):
        raise NotImplementedError()
