"""Application extensions instantiated here for import by modules.

This file keeps singletons (e.g. `db`) that are initialized by the
application factory in `app.py` to avoid circular imports.
"""

from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instance used across the application. Call `db.init_app(app)`
# in the factory to bind it to a Flask app.
db = SQLAlchemy()