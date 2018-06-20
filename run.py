import os

from app.app import create_app
from manage import migrate

config_name = "development"
app = create_app(config_name)

migrate(app)


if __name__ == '__main__':
    app.run(debug=True)