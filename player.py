"""Interface for player in TuringLeague game."""

class Player(object):

    def __init__(self, name, is_bot):
        self._name = name
        self._is_bot = is_bot

    def start_game(self, role, rounds):
        pass

    def send_message(self, message):
        pass

    def end_game(self, victory):
        pass

    def is_bot(self):
        return self._is_bot

    def name(self):
        return self._name
