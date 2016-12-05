from database import Database

#DEMO HOW TO USE THE DATABASE API

db = Database()

#top_users = db.get_top_users_table()
#print(top_users)

#top_bots = db.get_top_bots_table()
#print(top_bots)

#print(db.get_best_user())

#print(db.get_best_bot())

#db.increment_user_wins('Mihai')

#db.increment_user_loses('Mihai')

#db.increment_bot_wins('Optimus Prime')

#db.increment_bot_loses('Optimus Prime')

#db.add_user("Mia")
#db.add_bot("Schooby", "cleverbot")

print(db.does_user_exist('Mihai'))
print(db.does_user_exist('Pedro'))
