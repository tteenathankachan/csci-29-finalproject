# flask_s3_uploads/__init__.py


from .web_integration import app

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
