from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    done = db.Column(db.Boolean(), unique=False, nullable=False)
    label = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.label

    def serialize(self):
        return {
            "id": self.id,
            "done": self.done,
            "label" : self.label
            # do not serialize the password, its a security breach
        }