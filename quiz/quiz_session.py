import random


class QuizSession:
    def __init__(self, user, topic):
        self.session_id = id(self)
        self.user = user
        self.topic = topic
        self.items_queue = topic.items.copy()
        random.shuffle(self.items_queue)
        self.current_item = None
        self.score = 0

    def next_item(self):
        if not self.items_queue:
            return None

        self.current_item = self.items_queue.pop()
        return self.current_item

    def check_answer(self, answer: str):
        if self.current_item is None:
            return False

        is_correct = answer.strip().lower() == self.current_item.translation.lower()

        if is_correct:
            self.score += 1

        self.user.update_progress(self.topic.topic_id, is_correct)

        return is_correct

    def show_hint(self):
        if self.current_item:
            return self.current_item.hint
        return None
