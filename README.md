# Movie Watchlist (Django)

A full CRUD web app for tracking movies — add, edit, delete, search, and mark
movies as watched/unwatched. Built for the Full Stack Application Development
Assignment 1 (Django, PostgreSQL).

---

## Features

- Homepage listing all movies, newest first
- Add a new movie (inline form on the homepage)
- Edit an existing movie
- Delete a movie
- Mark a movie as Watched / Unwatched
- Search movies by title
- Dedicated Watchlist page showing Watched and Unwatched movies separately
- Django Admin panel for managing movies directly

---

## Tech Stack

- Python 3.12
- Django 6.0
- PostgreSQL
- HTML (no CSS framework — plain HTML/CSS)

---

## Setup Instructions

1. **Clone the repo**
   ```
   git clone <your-repo-url>
   cd movie_assignment
   ```

2. **Create and activate a virtual environment**
   ```
   python -m venv venv
   venv\Scripts\Activate.ps1        # Windows PowerShell
   # source venv/bin/activate       # macOS/Linux
   ```

3. **Install dependencies**
   ```
   pip install django psycopg[binary]
   ```

4. **Create the PostgreSQL database**
   Using `psql` or pgAdmin, create an empty database (e.g. `moviewatchlist_db`)
   and a user with access to it.

5. **Configure the database connection**
   In `watchlist_project/settings.py`, fill in `DATABASES` with your DB name,
   user, and password.

6. **Run migrations**
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create a superuser (for Django Admin)**
   ```
   python manage.py createsuperuser
   ```

8. **Run the development server**
   ```
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000/` for the app and `http://127.0.0.1:8000/admin/`
   for the admin panel.

---

## Project Structure

```
movie_assignment/
├── manage.py
├── watchlist_project/       # project config: settings, root urls
│   ├── settings.py
│   └── urls.py
└── movies/                  # the app: all movie logic lives here
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    └── templates/
        └── movies/
            ├── home.html
            ├── edit_movie.html
            └── watchlist.html
```

---

## Concepts Used Beyond the Lecture

The class lecture (*Django Fundamentals: Templates, Models, ORM & Forms*)
covered the core MVT flow, basic models/fields, `{% extends %}` /
`{% block %}` inheritance, plain ORM calls (`.all()`, `.filter()`,
`.create()`), and manual POST-handling forms with `request.POST.get()`.
This project builds on that foundation with a few additional pieces the
lecture didn't cover directly. Notes and doc links below.

### 1. Model field validators
```python
personal_rating = models.IntegerField(
    validators=[MinValueValidator(1), MaxValueValidator(5)]
)
```
`MinValueValidator` / `MaxValueValidator` restrict a numeric field to a
range. They run when a `ModelForm` or `full_clean()` validates the field —
they are **not** enforced automatically by `Model.objects.create()`, so
this project also does basic manual checks in the view.
📖 [Django Validators reference](https://docs.djangoproject.com/en/6.0/ref/validators/)

### 2. `Meta.ordering` on a model
```python
class Meta:
    ordering = ['-date_added']
```
Sets a default sort order for every query on the model, so `Movie.objects.all()`
already comes back newest-first without adding `.order_by()` everywhere.
📖 [Model Meta options — `ordering`](https://docs.djangoproject.com/en/6.0/ref/models/options/#ordering)

### 3. `get_object_or_404`
```python
movie = get_object_or_404(Movie, id=movie_id)
```
A shortcut that wraps a `.get()` lookup: if the object exists it's returned
as normal; if not, it raises `Http404` automatically instead of crashing
with an unhandled `DoesNotExist` error. Useful for edit/delete views where
the ID in the URL might not exist (e.g. already deleted, or a bad link).
📖 [Django shortcut functions](https://docs.djangoproject.com/en/6.0/topics/http/shortcuts/)

### 4. URL path converters with named URLs + `{% url %}`
```python
path("<int:movie_id>/edit/", views.edit_movie, name="edit_movie")
```
```django-html
<a href="{% url 'edit_movie' movie.id %}">Edit</a>
```
`<int:movie_id>` captures a number from the URL and passes it into the view
as an argument. Naming the URL (`name="edit_movie"`) lets templates build
links with `{% url %}` by name instead of hardcoding paths — if the URL
pattern ever changes, every link built with `{% url %}` still works.
📖 [URL dispatcher — path converters](https://docs.djangoproject.com/en/6.0/topics/http/urls/#path-converters)
📖 [`{% url %}` template tag](https://docs.djangoproject.com/en/6.0/ref/templates/builtins/#url)

### 5. Field lookups for search (`icontains`) + `request.GET`
```python
query = request.GET.get("q", "")
movies = movies.filter(title__icontains=query)
```
`request.GET` reads query-string parameters (from `?q=...` in the URL,
typically from a `method="get"` form) — different from `request.POST`,
which reads submitted form body data. `title__icontains` is a **field
lookup**: it filters rows where the title *contains* the search text,
case-insensitively.
📖 [Field lookups reference](https://docs.djangoproject.com/en/6.0/ref/models/querysets/#field-lookups)

### 6. Template filters (`yesno`)
```django-html
{{ movie.watched|yesno:"Yes,No" }}
```
A template filter transforms a variable's output. `yesno` converts a
boolean into custom text instead of printing Python's `True`/`False`.
📖 [Built-in template filters](https://docs.djangoproject.com/en/6.0/ref/templates/builtins/#yesno)

### 7. Multiple `<form>` elements per row, each needing its own CSRF token
Each Edit/Delete/Toggle action in the movie table is its own small
`<form method="post">` with its own `{% csrf_token %}` — every POST form on
a page needs its own token, not just one shared per page. Delete and Toggle
are intentionally POST-only (not plain `<a href>` links), so an accidental
click or a crawler visiting the link can't silently delete or change data.
📖 [Cross Site Request Forgery protection](https://docs.djangoproject.com/en/6.0/ref/csrf/)

---

## AI Tool Acknowledgment

**Tool used:** Claude (Anthropic), acting as a tutor/pair-programmer
throughout development.

**How it was used:**
- Explaining Django error messages and tracebacks (e.g. why `manage.py`
  commands run system checks that import `urls.py`, causing errors in one
  file to surface when running unrelated commands)
- Explaining unfamiliar concepts not covered in lecture, listed above
  (`get_object_or_404`, validators, field lookups, named URLs, etc.)
- Drafting this README
