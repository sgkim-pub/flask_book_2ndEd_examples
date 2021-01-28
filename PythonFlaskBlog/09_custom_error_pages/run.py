from flask import Flask, Blueprint, render_template

error = Blueprint('error', __name__)

@error.app_errorhandler(403)
def error403(error):
    print(error)
    return render_template('errors/403.html')

@error.app_errorhandler(404)
def error404(error):
    print(error)
    return render_template('errors/404.html')

@error.app_errorhandler(500)
def error500(error):
    print(error)
    return render_template('errors/500.html')

app = Flask(__name__)
app.register_blueprint(error)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run("127.0.0.1", 5000)
