from app import create_app

app = create_app()

if __name__ == "__main__":
    # taken from https://stackoverflow.com/questions/41940663/how-can-i-change-the-host-and-port-that-the-flask-command-uses
    app.run(host="0.0.0.0", port=5050, debug=True)