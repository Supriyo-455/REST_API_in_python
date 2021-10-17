from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from utils import destinations, message

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(600))
    country = db.Column(db.String(30), nullable=False)

    def __repr__(self) -> str:
        return f"{self.city} - {self.description} - {self.country}"


@app.route('/messages', methods=['GET'])
def get_message():
    return {"message": message}


@app.route('/destinations', methods=['GET'])
def get_destinations():
    data = Destination.query.all()
    output = []
    for destination in data:
        json_data = {"id": destination.id,
                     "city": destination.city,
                     "description": destination.description,
                     "country": destination.country}
        output.append(json_data)

    return {'destinations': output}


@app.route('/destinations/<id>', methods=['GET'])
def get_destination(id):
    destination = Destination.query.get_or_404(id)
    json_data = {"id": destination.id,
                 "city": destination.city,
                 "description": destination.description,
                 "country": destination.country}

    return json_data


@app.route('/destinations', methods=['POST'])
def add_destination():
    destination = Destination(
        city=request.json['city'],
        description=request.json['description'],
        country=request.json['country']
    )

    db.session.add(destination)
    db.session.commit()
    return {'id': destination.id}


@app.route('/destinations', methods=['DELETE'])
def delete_all():
    db.session.query(Destination).delete()
    db.session.commit()
    return {"message": "Deleted!"}


@app.route('/destinations/<id>', methods=['DELETE'])
def delete(id):
    destination = Destination.query.get(id)
    if destination is None:
        return {"error": "not found"}
    db.session.delete(destination)
    db.session.commit()
    return {"message": "Deleted!"}


@app.route('/destinations/<id>', methods=['PUT'])
def updateDestination(id):
    destination = Destination.query.get(id)
    if destination is None:
        return {"error": "not found"}

    # Update the data
    destination.city = request.json['city']
    destination.description = request.json['description']
    destination.country = request.json['country']

    # commit the changes
    db.session.commit()

    return {"id": destination.id,
            "city": destination.city,
            "description": destination.description,
            "country": destination.country}


@app.route('/')
def home():
    # Return welcome message to the client
    return 'Welcome! You are all set to go!'


@app.route('/initialize', methods=['GET'])
def setupDB():
    for item in destinations:
        data = Destination(
            city=item['city'],
            description=item['description'],
            country=item['country'])
        db.session.add(data)
        db.session.commit()

    return "Database Initialized!"


if __name__ == '__main__':
    app.run(debug=True)
