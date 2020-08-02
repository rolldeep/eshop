from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')


@app.route('/cart/')
def show_cart():
    return render_template('cart.html')


@app.route('/account/')
def show_account():
    return render_template('account.html')


@app.route('/login/')
def login():
    return render_template('login.html')


@app.route('/logout/')
def logout():
    return render_template('login.html')



if __name__ == "__main__":
    app.run(debug=True)