#!/usr/bin/env python3
from datetime import date, timedelta

from app import app
from models import Exercise, Workout, WorkoutExercise, db

with app.app_context():
    # Delete the join table first so foreign keys never dangle
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    exercises = [
        Exercise(name='Push-up', category='strength', equipment_needed=False),
        Exercise(name='Squat', category='strength', equipment_needed=False),
        Exercise(name='Dumbbell Curl', category='strength', equipment_needed=True),
        Exercise(name='Plank', category='core', equipment_needed=False),
        Exercise(name='Running', category='cardio', equipment_needed=False),
        Exercise(name='Rowing Machine', category='cardio', equipment_needed=True),
    ]
    db.session.add_all(exercises)
    db.session.commit()
    pushup, squat, curl, plank, running, rowing = exercises

    today = date.today()
    workouts = [
        Workout(date=today, duration_minutes=45, notes='Upper body focus'),
        Workout(date=today - timedelta(days=1), duration_minutes=30, notes='Cardio day'),
        Workout(date=today - timedelta(days=3), duration_minutes=60, notes='Full body'),
    ]
    db.session.add_all(workouts)
    db.session.commit()
    upper, cardio, full = workouts

    links = [
        WorkoutExercise(workout_id=upper.id, exercise_id=pushup.id, reps=15, sets=3),
        WorkoutExercise(workout_id=upper.id, exercise_id=curl.id, reps=12, sets=3),
        WorkoutExercise(workout_id=cardio.id, exercise_id=running.id, duration_seconds=1200),
        WorkoutExercise(workout_id=cardio.id, exercise_id=rowing.id, duration_seconds=600),
        WorkoutExercise(workout_id=full.id, exercise_id=squat.id, reps=10, sets=4),
        WorkoutExercise(workout_id=full.id, exercise_id=pushup.id, reps=20, sets=2),
        WorkoutExercise(workout_id=full.id, exercise_id=plank.id, sets=3, duration_seconds=60),
    ]
    db.session.add_all(links)
    db.session.commit()
    print('Seeded 6 exercises, 3 workouts, 7 workout exercises.')