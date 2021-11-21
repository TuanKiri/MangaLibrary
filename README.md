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

python db_create.py
```

Download Bootstrap 5 and add in app/static/js/bootstrap/, app/static/css/bootstrap/.

```cmd
$env:FLASK_APP = 'run.py'

flask run
```

<details><summary>Screenshots</summary>
Index page:

![index page](assets/2.png)

User profile:

![user profile](assets/1.png)

Manga page:

![manga page](assets/3.png)

Chapter page:

![chapter page](assets/4.png)

</details>
