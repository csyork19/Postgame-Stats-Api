class PostGameStatsException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"Post Game Stats API: {self.message}".to_dict()
