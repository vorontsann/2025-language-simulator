class Progress:
    def __init__(self, user_id):
        self.user_id = user_id
        self.per_topic_stats = {}   # {"Food": {"correct": 0, "incorrect": 0}}
        self.total_score = 0

    def record_result(self, topic_id: str, is_correct: bool):
        if topic_id not in self.per_topic_stats:
            self.per_topic_stats[topic_id] = {"correct": 0, "incorrect": 0}

        if is_correct:
            self.per_topic_stats[topic_id]["correct"] += 1
            self.total_score += 1
        else:
            self.per_topic_stats[topic_id]["incorrect"] += 1

    def get_summary(self):
        return {
            "total_score": self.total_score,
            "details": self.per_topic_stats
        }
