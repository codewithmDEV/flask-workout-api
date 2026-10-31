from marshmallow import Schema, ValidationError, fields, validate, validates_schema


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    category = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    equipment_needed = fields.Bool(load_default=False)


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str(allow_none=True)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(validate=validate.Range(min=1), allow_none=True)
    sets = fields.Int(validate=validate.Range(min=1), allow_none=True)
    duration_seconds = fields.Int(validate=validate.Range(min=1), allow_none=True)

    @validates_schema
    def require_reps_or_duration(self, data, **kwargs):
        if data.get('reps') is None and data.get('duration_seconds') is None:
            raise ValidationError('Provide reps or duration_seconds.')


class WorkoutExerciseDetailSchema(WorkoutExerciseSchema):
    exercise = fields.Nested(ExerciseSchema, dump_only=True)


class WorkoutDetailSchema(WorkoutSchema):
    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseDetailSchema), dump_only=True
    )


class ExerciseDetailSchema(ExerciseSchema):
    workouts = fields.List(fields.Nested(WorkoutSchema), dump_only=True)


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
exercise_detail_schema = ExerciseDetailSchema()
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_detail_schema = WorkoutDetailSchema()
workout_exercise_schema = WorkoutExerciseSchema()
workout_exercise_detail_schema = WorkoutExerciseDetailSchema()