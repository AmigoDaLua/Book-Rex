from flask import Flask, render_template, request, redirect
from cs50 import SQL

app = Flask(__name__)

db = SQL("sqlite:///recommendations.db") # setting db


@app.route("/", methods=["GET", "POST"])
def index():
    

    if request.method == "POST": # testing inputs
        title = request.form.get("title")
        author = request.form.get("author") or "unknown" # support for "unknown" authors
        reason = request.form.get("reason")

        # dealing with input errors:
        if not title:
            return "Please enter the book's name!"

        elif not reason:
            return "Please enter a reason. Any reason!"

        # all good? save the data!
        else:
            db.execute("INSERT INTO recommendations (title, author, reason) VALUES(?, ?, ?)", title, author, reason)
            return redirect("/recommendations")

    else:
        return render_template("index.html")


@app.route("/recommendations")
def recommendations():
    # getting data from database
    recs = db.execute("SELECT title, author, reason FROM recommendations ORDER BY title")
    # sending recs data to template
    return render_template("recommendations.html", recs=recs)

# starting the app
if __name__ == "__main__":
    app.run()