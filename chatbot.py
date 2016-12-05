"""ChatBot implementation of Player."""
from player import Player
import time
import random

class ChatBot(Player):

    def __init__(self, name, session, bot_type, db):
        super(ChatBot, self).__init__(name, True)
        self._session = session
        self._bot_type = bot_type
        self._db = db

    def set_game(self, game):
        self._game = game

    def start_game(self, role, rounds):
        pass

    def send_message(self, message):
        time.sleep(random.randint(10, 15))
        self._game.defender_message(self._session.think(message))

    def end_game(self, victory):
        if not self._db.does_bot_exist(self.name()):
            self._db.add_bot(self.name(), self._bot_type)

        if victory:
            self._db.increment_bot_wins(self.name())
        else:
            self._db.increment_bot_loses(self.name())
