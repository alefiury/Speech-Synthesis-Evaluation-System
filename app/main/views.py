#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, send_from_directory, send_file, session, url_for, redirect, flash
from flask_login import login_required, current_user
from . import main
from .forms import VoteForm
from .. import db

from io import BytesIO
import os
import glob

# Quantity of audios to be evaluated
AUDIO_LIMIT = 5

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

@main.route('/', methods=['GET', 'POST'])
@login_required
def hello():
  form = VoteForm()
  audio_filepaths = glob.glob(os.path.join('audios', '*.wav'))

  lines = get_text_and_audiopath(filepath='test_audiopaths.csv')

  if current_user.last_audio == None:
    idx = 0
  else:
    idx = current_user.last_audio

  if idx >= AUDIO_LIMIT or idx >= len(lines):
    flash('Votação concluida com sucesso', 'success')

  if form.validate_on_submit():
    with open('score.csv', 'a+') as score:
      score.write(f'{current_user.id}|{os.path.basename(lines[idx][0])}|{os.path.basename(lines[idx][1])}|{form.score.data}\n')
    current_user.last_audio = idx + 1
    db.session.add(current_user)
    db.session.commit()
    return redirect(url_for('main.hello'))

  return render_template('home.html', paths=lines, idx=idx, audio_limit=AUDIO_LIMIT, max_lenth=len(lines), form=form, os=os)

@main.route('/play/<filename>')
def download_file(filename):
  audio_file = open(os.path.join('.', 'audios', filename), 'rb')
  audio_bytes = audio_file.read()
  return send_file(BytesIO(audio_bytes), attachment_filename=filename, mimetype="audio/wav")