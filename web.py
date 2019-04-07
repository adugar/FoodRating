from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/thanks')
def thanks():
    return render_template("thanks.html")

@app.route('/review/<date>')
def hello(date):
    return render_template("rating.html", date=date)

@app.route('/review/<date>', methods=['POST'])
def hello_post(date):
    s = request.form['text']
    a = request.form['dropdown']
    print(s)
    print(a)
    return redirect('/thanks')


if __name__ == '__main__':
    app.run(debug=True)