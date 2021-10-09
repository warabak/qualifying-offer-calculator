from calculator import create_app

app = create_app()
app.logger.info("We have just created a Flask app!")

if __name__ == "__main__":
    app.logger.info("It looks like we're running locally via __main__...starting the app in debug mode")
    app.run(debug=True, host="0.0.0.0")
