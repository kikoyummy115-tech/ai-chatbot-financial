from flask import Flask, render_template


app = Flask(__name__)



@app.route("/chat", methods=["GET"])
def ai_chat():
    
    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)