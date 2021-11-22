# MangaLibrary

Simple manga reader application written on flask with SQLite database.

## Features

- user profile, manga commenting, subscription on user / manga
- add manga, add chapter, update manga, tags
- post news
- user rating
- administrator moderate comments

## Installation for Windows ![Windows](assets/5.png)

```cmd
git clone https://github.com/JC5LZiy3HVfV5ux/MangaLibrary.git

cd MangaLibrary

python -m venv env

.\env\Scripts\activate

pip install -r requirements.txt
```

⚠️ [Bugs in flask_uploads package](https://stackoverflow.com/questions/61628503/flask-uploads-importerror-cannot-import-name-secure-filename)

```
python db_create.py
```

Download Bootstrap 5 and add in app/static/js/bootstrap/, app/static/css/bootstrap/.

```cmd
$env:FLASK_APP = 'run.py'

flask run
```
## Testing

Run unittest:

```
flask test
```

Run unittest using test_names:

```
flask test tests.test_basics   
```

Obtaining code coverage reports:

```
flask test --coverage
```

## Screenshots
<details><summary>Open</summary>
Index page:

![index page](assets/2.png)

User profile:

![user profile](assets/1.png)

Manga page:

![manga page](assets/3.png)

Chapter page:

![chapter page](assets/4.png)

</details>
