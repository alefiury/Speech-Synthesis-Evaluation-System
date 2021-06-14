#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, send_from_directory, send_file, session, url_for, redirect, flash
from flask_login import login_required, current_user
from . import main
from .forms import VoteForm, PageForm

import os
import glob
import random
from io import BytesIO
from datetime import datetime
from pathlib import Path

from boto3 import resource, client
import pyrebase

from config import Config
from .. import (bucket, s3_resource,
                s3_client, firebase_db,
                audio_filepaths_orig, max_lenth, db)

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

  # Message after the evaluation of all samples
  if session['idx'] >= max_lenth:
    flash('Votação concluida com sucesso', 'success')

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

  return render_template('home.html', vote_form=vote_form, page_form=page_form, session=session, max_lenth=max_lenth, audio_filepaths=audio_filepaths, s3_client=s3_client)