# Quality Evaluation System for Speech Synthesis

A web application developed in flask for quality evaluation of synthesized speech in brazilian portuguese, based on Mean Opinion Score (MOS).

The evaluation takes into account 5 possible scores: Excellent, Good, Fair, Poor and Bad.

# How the Application Works

Every participant can choose beetween 5 possible values for each audio sample.

Every audio sample provided will be shown one by one.

When all samples are evaluated, the participant will not be able to evaluate more samples.

To minimize bias during the evaluation, the audio samples are shown in a random order for each participant, and even after a logout,
the participants will be able to continue to evaluate the samples from where they stopped.

## 1. Dependencies

To install the necessary dependencies via pip:

```
$ sudo pip install -r requeriments
```

## 2. Set Environment Variables

To sucessfully run the application you need to set the environment variables that are used to handle encryption and data storage.

These variables can be seen and set in the config file.

### 2.2 Score Database

The scores given by the users are saved in a RealTime Database on the Firebase platform. Is necessary that you create an account, add a new app project, get the information related to the project and set the enviroment variables that are related with the RealTime Database.

More information can be found [here](https://firebase.google.com).

### 2.3 Audio Database

The audios that will be evaluated need to be stored in a AWS S3 Storage bucket. Set the environment variables related with the S3 storage accordingly.

### 2.4 Volume Test

The audio used as a volume tester also need to be stored in a AWS S3 Storage bucket, in a different bucket from the evaluation data. Set the environment variables accordingly.

## 3. Secret key

Choose your own secret key. As an example, you could use the result from the following script:

```
$ python -c 'import os; print(os.urandom(24))'
```

## 4. User Information Database

In order to create the database necessary to save the information of your users, run the following bash command:

```
$ export FLASK_APP=main.py
$ flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
```

## 5. Execute

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

## Deployment

The application is already prepared to be deployed to Heroku.

More information on deployment using Git can be found [here](https://devcenter.heroku.com/articles/git).

## Author

- Alef Iury S. Ferreira

## Contact

- e-mail: alef_iury_c.c@discente.ufg.br
