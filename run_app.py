#!/usr/bin/python

from WMS import db
from WMS import create_app

app = create_app()

if __name__ == "__main__":
    app.run()