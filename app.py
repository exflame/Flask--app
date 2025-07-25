from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'replace-with-a-secret'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/free'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Message(db.Model):
    __tablename__ = 'messages' 
    id         = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50),  nullable=False)
    last_name  = db.Column(db.String(50),  nullable=False)
    email      = db.Column(db.String(120), nullable=False)
    body       = db.Column(db.Text,        nullable=False)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/contact', methods=['POST'])
def create_message():
    msg = Message(
        first_name = request.form['first_name'],
        last_name  = request.form['last_name'],
        email      = request.form['email'],
        body       = request.form['message']
    )
    db.session.add(msg)
    db.session.commit()
    flash('Message sent!', 'success')
    return redirect(url_for('messages'))

@app.route('/messages')
def messages():
    all_msgs = Message.query.order_by(Message.id.desc()).all()
    return render_template('messages.html', messages=all_msgs)

@app.route('/messages/<int:id>/edit')
def edit_message(id):
    msg = Message.query.get_or_404(id)
    return render_template('edit.html', msg=msg)

@app.route('/messages/<int:id>/update', methods=['POST'])
def update_message(id):
    msg = Message.query.get_or_404(id)
    msg.first_name = request.form['first_name']
    msg.last_name  = request.form['last_name']
    msg.email      = request.form['email']
    msg.body       = request.form['body']
    db.session.commit()
    flash(f'Message #{id} updated.', 'info')
    return redirect(url_for('messages'))

@app.route('/messages/<int:id>/delete', methods=['POST'])
def delete_message(id):
    msg = Message.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    flash(f'Message #{id} deleted.', 'warning')
    return redirect(url_for('messages'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
