from flask_babel import _
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import RadioField, SubmitField

class VoteForm(FlaskForm):
  score = RadioField(_l('Avaliação'), choices = [1, 2, 3, 4, 5],  validators=[DataRequired()])
  submit_next = SubmitField(_l('Próximo'))

class PageForm(FlaskForm):
  submit_prev = SubmitField(_l('Anterior'))