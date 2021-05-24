# Quality Evaluation System for Speech Synthesis

This is a web application developed in flask for quality evaluation of synthesized speech in brazilian portuguese, based on Mean Opinion Score (MOS).

The evaluation takes into account 5 possible scores: Excellent, Good, Fair, Poor and Bad.

## 1. Dependencies

To install the necessary dependencies via pip:

```
$ sudo pip install -r requeriments
```

## 2. Database

To create and set the database:

```
$ export FLASK_APP=main.py
$ flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
```

## 3. Secret key

Set your own secret key in the config.py file. As an example, you can use the result from the following script:

```
$ python -c 'import os; print(os.urandom(24))'
```

## 4. Audios for Evaluation

Create the following directory and add the audios to be evaluated in there:

```
$ mkdir audios
```

Or you can create any directory outside of 'app' directory and add the audios there. In this case, you
just need to change the path in 'AUDIO_PATH' located in the view file in the app/main directory.

## 5. Volume Test

Create the following directory and add the audio with the name 'sound_text.audio_extension' that will be used as the volume tester:

```
$ mkdir sound_test
```

## 6. Execute

To run the application, run the following bash command:

```
$ bash start_app.sh
```

## Migration

In order to migrate your database:

```
$ flask db init
$ flask db migrate -m "your_migration"
```

## Author

- Alef Iury S. Ferreira

## Contact

- e-mail: alef_iury_c.c@discente.ufg.br
