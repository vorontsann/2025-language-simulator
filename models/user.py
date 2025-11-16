from .progress import Progress


class User:
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username
        self.selected_language = None
        self.progress = Progress(user_id)

    def select_language(self, lang):
        self.selected_language = lang

    def update_progress(self, topic_id, is_correct):
        self.progress.record_result(topic_id, is_correct)
