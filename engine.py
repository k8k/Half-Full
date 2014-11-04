from flask import Flask, redirect, render_template
import os

app = Flask(__name__)
app.secret_key= 'katekuchinproject'


GOOGLE_MAPS_EMBED_KEY = os.environ.get("GOOGLE_MAPS_EMBED_KEY")

@app.route("/")
def half_full_home():   
    return render_template("index.html")



@app.route("/location")
def user_location():
	return render_template("results.html", GOOGLE_MAPS_EMBED_KEY=GOOGLE_MAPS_EMBED_KEY)


if __name__ == "__main__":
    app.run(debug = True)