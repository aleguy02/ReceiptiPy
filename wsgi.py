# wsgi stands for Web Server Gateway Interface.
# This code was adapted from multiple sources, I recommend:
# "How to Deploy Flask with Gunicorn and Nginx (on Ubuntu)" from Tony Teaches Tech on YouTube
# =====================================================
from app import app

if __name__ == "__main__":
    app.run()