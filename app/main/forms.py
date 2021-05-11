from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import RadioField, SubmitField

class VoteForm(FlaskForm):
  score = RadioField('Avaliação', choices = [1, 2, 3, 4, 5],  validators=[DataRequired()])
  submit = SubmitField('Próximo')