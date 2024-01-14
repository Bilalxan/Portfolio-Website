from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from forms import ContactForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'itisforpersonalwebsite'
Bootstrap5(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
db = SQLAlchemy()
db.init_app(app)

# Configure table
class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    message = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        new_message = Messages(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data,
        )
        db.session.add(new_message)
        db.session.commit()
        return redirect("/")
    return render_template("contact.html", form=form)

app.run(debug=True)


