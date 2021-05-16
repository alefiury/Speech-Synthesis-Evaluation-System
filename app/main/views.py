#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, send_from_directory, send_file, session, url_for, redirect, flash
from flask_login import login_required, current_user
from . import main
from .forms import VoteForm
from .. import db

from io import BytesIO
import random
from datetime import datetime
import os
import glob
from pathlib import Path

# Quantity of audios to be evaluated
AUDIO_PATH = 'audios'

def get_text_and_audiopath(filepath):
  """
  Gets the audio filenames and texts from a csv file.

  -----

  Args:
    filepath: Filepath to the csv file, must be in the format: filename|text.

  Returns:
    Bidimensional list, first element: filename, second element: text.
  """
  with open(filepath, 'r') as f:
    lines = [line.rstrip().split('|') for line in f.readlines()]

  return lines

@main.route('/sound_test', methods=['GET', 'POST'])
@login_required
def sound_test():
  return render_template('sound_test.html')

@main.route('/introduction', methods=['GET', 'POST'])
@login_required
def introduction():
  return render_template('introduction.html')

@main.route('/', methods=['GET', 'POST'])
@login_required
def hello():
  form = VoteForm()
  # First access
  if current_user.seed == None and current_user.last_audio == None:
    # Set seed to shuffle audio file paths
    session['seed'] = datetime.now()
    current_user.seed = session['seed']

    # Set index
    session['idx'] = 0
    current_user.last_audio = session['idx']

    # Saves in the database
    db.session.add(current_user)
    db.session.commit()
    return redirect(url_for('main.hello'))
  else:
    session['seed'] = current_user.seed
    session['idx'] = current_user.last_audio

  # Set the audio filepaths
  session['audio_filepaths'] = glob.glob(os.path.join(AUDIO_PATH, '*.wav'))
  session['max_lenth'] = len(session['audio_filepaths'])

  # Shuffle audio file paths
  random.Random(session['seed']).shuffle(session['audio_filepaths'])

  # Message after evaluate all examples
  if session['idx'] >= len(session['audio_filepaths']):
    flash('Votação concluida com sucesso', 'success')

  if form.validate_on_submit():
    with open('score.csv', 'a+') as score:
      score.write(f"{current_user.id}|{os.path.basename(session['audio_filepaths'][session['idx']])}|{form.score.data}\n")

    session['idx'] += 1
    current_user.last_audio = session['idx']

    db.session.add(current_user)
    db.session.commit()

    return redirect(url_for('main.hello'))

  return render_template('home.html', form=form, session=session, os=os)

@main.route('/play/<path:filepath>')
def download_file(filepath):
  audio_file = open(os.path.join('.', filepath), 'rb')
  audio_bytes = audio_file.read()
  return send_file(BytesIO(audio_bytes), attachment_filename=os.path.basename(filepath), mimetype="audio/wav")