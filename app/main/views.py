#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import glob
import random
from io import BytesIO
from datetime import datetime
from pathlib import Path

import pyrebase
from flask_babel import _
from boto3 import resource, client
from flask_login import login_required, current_user
from flask import Blueprint, render_template, send_from_directory, send_file, session, url_for, redirect, flash, g

from config import Config
from . import main
from .forms import VoteForm, PageForm
from .. import (
  bucket, s3_resource,
  s3_client, firebase_db,
  audio_filepaths_orig, max_lenth, db
)

multilingual = Blueprint('multilingual', __name__, template_folder='templates', url_prefix='/<lang_code>')

@multilingual.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.lang_code)

@multilingual.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')

@main.route('/sound_test', methods=['GET', 'POST'])
@login_required
def sound_test():
  return render_template('sound_test.html', s3_client=s3_client, os=os)


@main.route('/introduction', methods=['GET', 'POST'])
@login_required
def introduction():
  return render_template('introduction.html')


@main.route('/', methods=['GET', 'POST'])
@login_required
def hello():
  # Make a copy of the audio paths for further processing
  audio_filepaths = audio_filepaths_orig[:]
  # Vote form, with the 'next' button
  vote_form = VoteForm()
  # Form used to introduce the 'previous' button
  page_form = PageForm()

  # First access to the application
  if current_user.seed == None and current_user.last_audio == None:
    # Set seed to shuffle audio filepaths
    session['seed'] = datetime.now()
    current_user.seed = session['seed']

    # Set index
    session['idx'] = 0
    current_user.last_audio = session['idx']

    # Saves seed and index in the local database
    db.session.add(current_user)
    db.session.commit()
    return redirect(url_for('main.hello'))
  else:
    session['seed'] = current_user.seed
    session['idx'] = current_user.last_audio

  # Shuffle audio file paths
  random.Random(session['seed']).shuffle(audio_filepaths)

  audio_filepaths = audio_filepaths[:int(Config.MAX_SAMPLES)]

  # Message after the evaluation of all samples
  if session['idx'] >= max_lenth:
    flash(_('Votação concluida com sucesso'), 'success')

  # 'previous' button
  if page_form.validate_on_submit() and page_form.submit_prev.data == True:
    # The index is subtracted if the 'previous' button is pressed
    session['idx'] -= 1
    current_user.last_audio = session['idx']
    db.session.add(current_user)
    db.session.commit()
    return redirect(url_for('main.hello'))

  elif vote_form.validate_on_submit():
    # Saves user's score into the firebase's realtime database
    score_data = {"score": vote_form.score.data}
    firebase_db.child(f"audio/{os.path.basename(audio_filepaths[session['idx']].key.split('.wav')[0])}/id_{current_user.id}").set(score_data)
    # Iterate the index and saves in the database
    session['idx'] += 1
    current_user.last_audio = session['idx']
    db.session.add(current_user)
    db.session.commit()
    return redirect(url_for('main.hello'))

  return render_template('home.html', vote_form=vote_form, page_form=page_form, session=session, max_lenth=len(audio_filepaths), audio_filepaths=audio_filepaths, s3_client=s3_client)