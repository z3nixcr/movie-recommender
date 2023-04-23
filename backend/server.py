import requests
import pickle as pkl

MOVIE_API_PATH = 'https://api.themoviedb.org/3/movie/'
MOVIE_POSTER_PATH = 'https://image.tmdb.org/t/p/w500/'
API_CODE = 'e8555078570d651dabc48e7d6768f5e6'


def fetch_movie_poster(movie_id):
    response = requests.get(f'{MOVIE_API_PATH}{movie_id}?api_key={API_CODE}&language=en-US')
    data = response.json()
    return MOVIE_POSTER_PATH + data['poster_path']


def get_movies():
    with open('movie_data_list.txt', 'r') as f:
        data = f.readlines()
        movies = [movie.strip() for movie in data]
        return movies


class Movie:
    def __init__(self):
        self.movies_with_posters = []

    def add_movie_poster(self, title, poster):
        movie = {'title': title, 'poster': poster}
        self.movies_with_posters.append(movie)

    def construct_movies(self, movies, posters):
        self.movies_with_posters.clear()
        for i in range(len(movies)):
            self.add_movie_poster(movies[i], posters[i])


class Recommender:
    def __init__(self):
        self.movies_data = pkl.load(open('movies.pkl', 'rb'))
        self.movies_list = (title for title in self.movies_data['title'].values)
        with open('movie_data_list.txt', 'w', encoding='UTF-8') as f:
            for movie_title in self.movies_list:
                f.write(f"{movie_title}\n")
        self.similarity = pkl.load(open('similarity.pkl', 'rb'))

    def recommend(self, movie):
        movie_index = self.movies_data[self.movies_data['title'] == movie].index[0]
        distances = self.similarity[movie_index]
        movies_sorted_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:9]

        recommended_movies = []
        recommended_movies_posters = []

        for position in movies_sorted_list:
            movie_id = self.movies_data.iloc[position[0]].movie_id
            recommended_movies.append(self.movies_data.iloc[position[0]].title)
            recommended_movies_posters.append(fetch_movie_poster(movie_id))

        return recommended_movies, recommended_movies_posters


if __name__ == "__main__":
    mrs = Recommender()
