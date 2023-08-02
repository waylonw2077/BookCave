from flask_migrate import Migrate, MigrateCommand
from app import create_app, db

app = create_app()
# manager = Manager(app)

# # # Initialize Flask-Migrate
# # migrate = Migrate(app, db)

# # Add the 'db' command to the manager
# manager.add_command('db', MigrateCommand)

# if __name__ == '__main__':
#     manager.run()
