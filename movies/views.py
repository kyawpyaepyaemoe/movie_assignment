from django.shortcuts import redirect, render, get_object_or_404

from .models import Movie

# Create your views here.
def home(request):

    error = None

    if request.method == "POST":
        title = request.POST.get("title")
        genre = request.POST.get("genre")
        release_year = request.POST.get("release_year")
        personal_rating = request.POST.get("personal_rating")

        if not title or title.strip() == "":
            error = "Title cannot be empty."
        else:
            Movie.objects.create(
                title=title,
                genre=genre,
                release_year=release_year or None,
                personal_rating=personal_rating or None,
            )
            return redirect("/")

    query = request.GET.get("q", "")
    movies = Movie.objects.all()
    if query:
        movies = movies.filter(title__icontains=query)

    total_movies = movies.count()
    watched_movies = movies.filter(watched=True).count()
    unwatched_movies = movies.filter(watched=False).count()

    context = {
        "movies": movies,
        "error": error,
        "query": query,
        "total_movies": total_movies,
        "watched_movies": watched_movies,
        "unwatched_movies": unwatched_movies,
    }

    return render(request, "movies/home.html", context)


def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == "POST":
        title = request.POST.get("title")
        if not title or title.strip() == "":
            return render(request, "movies/edit_movie.html", {"movie": movie, "error": "Title cannot be empty."})

        movie.title = title
        movie.genre = request.POST.get("genre")
        movie.release_year = request.POST.get("release_year") or None
        movie.personal_rating = request.POST.get("personal_rating") or None
        movie.save()
        return redirect("/")

    return render(request, "movies/edit_movie.html", {"movie": movie})


def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == "POST":
        movie.delete()
    return redirect("/")


def toggle_watched(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    movie.watched = not movie.watched
    movie.save()
    return redirect("/")

def watchlist(request):
    watched_movies = Movie.objects.filter(watched=True)
    unwatched_movies = Movie.objects.filter(watched=False)

    context = {
        "watched_movies": watched_movies,
        "unwatched_movies": unwatched_movies,
    }

    return render(request, "movies/watchlist.html", context)