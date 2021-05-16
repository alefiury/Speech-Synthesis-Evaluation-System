# Quality Evaluation System for Speech Synthesis

This is a web application developed in flask for quality evaluation of synthesized speech in brazilian portuguese, based on Mean Opinion Score (MOS)

The evaluation takes into account 5 possible scores: Excellent, Good, Medium, Poor and Bad.

## 1. Dependencies

To install the necessary dependencies via pip:

```
$ sudo pip install -r requeriments
```

## Database

To create the database:

```
$ export FLASK_APP=main.py
$ flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
```

## Migration

To migrate your database:

```
$ flask db init
$ flask db migrate -m "name_of_your_migration"
```

## Audios for Evaluation

Create the following directory and add the audios to be evaluated in there:

```
$ mkdir audios
```

Or you can create any directory outside of 'app', and add the audios there. In this case you
just need to change the path in 'AUDIO_PATH' in the config file.

## Audio for Sound Test

Create the following directory and add the audio that will be used as the sound tester:

```
$ mkdir sound_test
```

## 2. Execute

To run the application, run the following bash command:

```
$ bash start_app.sh
```

## Author

- Alef Iury S. Ferreira

## Contact

- e-mail: alef_iury_c.c@discente.ufg.br
