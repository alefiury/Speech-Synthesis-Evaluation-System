# Quality Evaluation System for Speech Synthesis

This is a evaluation web aplication developed in flask for speech synthesis.

Users can give a score, given a synthesized speech and its respective text, the results are saved
in a csv file.

## 1. Dependencies

To install the necessary dependencies via pip, run:

```
$ sudo pip install -r requeriments
```

## Database

To create the database, simply run:

```
$ export FLASK_APP=main.py
$ flask shell
$ from app import db
$ db.create_all()
$ exit()
```

## Migration

To migrate your database, run:

```
$ flask db init
$ flask db migrate -m "write_the_name_of_your_migration"
```

## 2. Run

To run the application, run the following bash command:

```
$ bash start_app.sh
```

## Author

- Alef Iury (UFG, Instituto de Informática)

## Contact

e-mail: alef_iury_c.c@discente.ufg.br
