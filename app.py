from flask import Flask,render_template
import pandas as pd

app = Flask(__name__)

@app.route("/")

def dashboard():

    df = pd.read_csv("attendance/attendance.csv")

    table = df.to_html(classes="data",index=False)

    return render_template(
        "dashboard.html",
        table=table
    )

if __name__ == "__main__":
    app.run(debug=True)