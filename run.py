#!/usr/bin/env python3

from app import create_app

app = create_app()

if __name__ == "__main__":
    # Debug=True is fine for local dev, but turn it off for production!
    app.run(host="0.0.0.0", port=5000, debug=True)
