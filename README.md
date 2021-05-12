# Quality Evaluation System for Speech Synthesis

This is a web application developed in flask for quality evaluation of synthesized speech in brazilian portuguese.

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
$ from app import db
$ db.create_all()
$ exit()
```

## Migration

To migrate your database:

```
$ flask db init
$ flask db migrate -m "name_of_your_migration"
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
