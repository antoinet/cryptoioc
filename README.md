## References
 * https://medium.com/the-andela-way/how-i-developed-an-api-in-python-using-flask-4e388674f1
 * https://medium.com/the-andela-way/deploying-a-python-flask-app-to-heroku-41250bda27d0
 * https://github.com/jokamjohn/bucket_api_heroku/blob/f3f9380c069b5a0a5d5116f2bd0ae1882c90ec69/app/models.py
 * https://hub.docker.com/_/postgres/
 * https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xviii-deployment-on-heroku
 
 
## local docker postgres

```bash
$ docker run --rm --name heroku-postgres -e POSTGRES_PASSWORD=password1 -d -p 5432:5432 postgres
$ docker run -it --rm --link heroku-postgres:postgres postgres psql -h postgres -U postgres
Password for user postgres:
psql (10.1)
Type "help" for help.

postgres=# CREATE DATABASE cryptoioc;
CREATE DATABASE
postgres=# CREATE USER cryptoioc WITH ENCRYPTED PASSWORD 'password1';
CREATE ROLE
postgres=# GRANT ALL PRIVILEGES ON DATABASE cryptoioc TO cryptoioc;
GRANT
```

## local dev environment
```bash
$ flask shell
>>> from app import db
>>> db.create_all()
>>> ...
```