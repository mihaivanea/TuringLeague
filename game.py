class Game(object):
    _ROUNDS = 10

    def __init__(self, attacker, defender, players_in_game):
        self._attacker = attacker
        
        if defender.is_bot():
            defender.set_game(self)

        self._defender = defender
        self._attacker.start_game('attacker', self._ROUNDS)
        self._defender.start_game('defender', self._ROUNDS)
        self._players_in_game = players_in_game

    def message(self, username, message):
        if self._attacker.name() == username:
            self.attacker_message(message)
        else:
            self.defender_message(message)

    def attacker_message(self, message):
        self._defender.send_message(message)

    def defender_message(self, message):
        self._attacker.send_message(message)

    def player_forfeit(self, username):
        if self._attacker.name() == username:
            self._defender.end_game(True)
        else:
            self._attacker.end_game(True)

        del self._players_in_game[self._attacker]
        if not self._defender.is_bot():
            del self._players_in_game[self._defender]

    def attacker_guess(self, is_bot):
        # remove players from game
        del self._players_in_game[self._attacker]

        if not self._defender.is_bot():
            del self._players_in_game[self._defender]

        if self._defender.is_bot() == is_bot:
            self._attacker.end_game(True)
            self._defender.end_game(False)
        else:
            self._attacker.end_game(False)
            self._defender.end_game(True)
