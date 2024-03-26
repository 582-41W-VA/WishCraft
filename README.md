# Project 2

### WishCraft

## Groupe member

- Aleksandra
- André
- Andres
- Maiko
- Tischa



## Installation instruction:

- Create Virtual Environment ```python -m venv .venv```
- Activate the Virtual Environment 
For Unix/macOS: ```source .venv/bin/activate```
For Windows: ```.venv\Scripts\activate```
- Install Django ```pip install django```
- Verify Installation
```python -m django --version```
- Install pillow to add image processing capabilities
```pip install pillow```
- Make migration
```python manage.py makemigrations app```
- Update migration
```python manage.py migrate```
- Create username for admin ```python manage.py createsuperuser```
- Start the server ```python3 manage.py runserver```

Note: if you are on mac you might need to use ```python3```

## Project architecture:

We were following Django general architecture with separating views according its function in the logic (authentication.py - login, sign up, sign out, cards.py - all manipulations with cards data)

```
app/
├── views/
│   ├── __init__.py
│   ├── authentication.py
│   ├── cards.py
│   └── ...
└── apps.py
```