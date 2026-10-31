# Flask Workout API

A Flask + SQLAlchemy + Marshmallow backend for a workout tracking app used by personal trainers. Workouts can include many reusable exercises, each with reps, sets, or duration. Validation is enforced at three levels: database table constraints, model validations, and schema validations.

## Installation

```
pipenv install
pipenv shell
cd server
export FLASK_APP=app.py
flask db upgrade head
python seed.py
```

## Running the app

```
python app.py
```

The API runs at http://localhost:5555.

## Endpoints

- `GET /workouts`: list all workouts.
- `GET /workouts/<id>`: show one workout with its exercises, including reps/sets/duration. 404 if not found.
- `POST /workouts`: create a workout (`date`, `duration_minutes`, optional `notes`). 201, or 422 if invalid.
- `DELETE /workouts/<id>`: delete a workout and its workout exercises. 204, or 404.
- `GET /exercises`: list all exercises.
- `GET /exercises/<id>`: show one exercise with the workouts it appears in. 404 if not found.
- `POST /exercises`: create an exercise (`name`, `category`, optional `equipment_needed`). 201, 422 if invalid, 409 if the name exists.
- `DELETE /exercises/<id>`: delete an exercise and its workout exercises. 204, or 404.
- `POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises`: add an exercise to a workout (`reps` and/or `duration_seconds`, optional `sets`). 201, 422 if invalid, 404 if either id is missing.

## Validations

- **Table constraints:** unique exercise name, `NOT NULL` columns, and `CHECK` constraints for positive duration, reps, sets, and seconds.
- **Model validations:** non-empty exercise name and category, positive workout duration, positive reps/sets/seconds.
- **Schema validations:** required fields, length and range checks, and a rule that a workout exercise needs reps or a duration.