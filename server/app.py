from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import Exercise, Workout, WorkoutExercise, db
from schemas import (
    exercise_detail_schema,
    exercise_schema,
    exercises_schema,
    workout_detail_schema,
    workout_exercise_detail_schema,
    workout_exercise_schema,
    workout_schema,
    workouts_schema,
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)


def error(message, status):
    return {'error': message}, status


@app.get('/workouts')
def list_workouts():
    return jsonify(workouts_schema.dump(Workout.query.all())), 200


@app.get('/workouts/<int:id>')
def show_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return error('Workout not found.', 404)
    return jsonify(workout_detail_schema.dump(workout)), 200


@app.post('/workouts')
def create_workout():
    try:
        data = workout_schema.load(request.get_json(silent=True) or {})
        workout = Workout(**data)
    except ValidationError as err:
        return {'errors': err.messages}, 422
    except ValueError as err:
        return error(str(err), 422)

    db.session.add(workout)
    db.session.commit()
    return jsonify(workout_schema.dump(workout)), 201


@app.delete('/workouts/<int:id>')
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return error('Workout not found.', 404)
    db.session.delete(workout)  # cascade also removes its WorkoutExercises
    db.session.commit()
    return make_response('', 204)


@app.get('/exercises')
def list_exercises():
    return jsonify(exercises_schema.dump(Exercise.query.all())), 200


@app.get('/exercises/<int:id>')
def show_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return error('Exercise not found.', 404)
    return jsonify(exercise_detail_schema.dump(exercise)), 200


@app.post('/exercises')
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json(silent=True) or {})
        exercise = Exercise(**data)
    except ValidationError as err:
        return {'errors': err.messages}, 422
    except ValueError as err:
        return error(str(err), 422)

    try:
        db.session.add(exercise)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return error('An exercise with that name already exists.', 409)
    return jsonify(exercise_schema.dump(exercise)), 201


@app.delete('/exercises/<int:id>')
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return error('Exercise not found.', 404)
    db.session.delete(exercise)  # cascade also removes its WorkoutExercises
    db.session.commit()
    return make_response('', 204)


@app.post('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises')
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)
    if not workout or not exercise:
        return error('Workout or exercise not found.', 404)

    try:
        data = workout_exercise_schema.load(request.get_json(silent=True) or {})
        link = WorkoutExercise(workout_id=workout.id, exercise_id=exercise.id, **data)
    except ValidationError as err:
        return {'errors': err.messages}, 422
    except ValueError as err:
        return error(str(err), 422)

    db.session.add(link)
    db.session.commit()
    return jsonify(workout_exercise_detail_schema.dump(link)), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)