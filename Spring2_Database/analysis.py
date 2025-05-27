import pandas as pd
import matplotlib.pyplot as plt

def main():
    df = pd.read_csv('imdb_top_1000.csv')

    df['No_of_Votes'] = df['No_of_Votes'].astype(int)
    df['IMDB_Rating'] = df['IMDB_Rating'].astype(float)
    df['Gross'] = df['Gross'].str.replace(',', '').astype(float)

    # Genre Analysis
    # Split the Genre string into lists, then explode to one-genre-per-row
    df['Genre'] = df['Genre'].str.split(', ')
    genres = df.explode('Genre')

    # Compute average votes (proxy for views) per genre
    avg_votes = (
        genres
        .groupby('Genre')['No_of_Votes']
        .mean()
        .sort_values(ascending=False)
    )

    # Compute average IMDB rating per genre
    avg_rating = (
        genres
        .groupby('Genre')['IMDB_Rating']
        .mean()
        .sort_values(ascending=False)
    )

    # Actor Analysis
    # Combine the four Star columns into one list and explode
    df['Actors'] = df[['Star1','Star2','Star3','Star4']].values.tolist()
    actors = df.explode('Actors')

    # Count how many movies each actor appears in
    actor_counts = actors['Actors'].value_counts()

    # Compute average IMDB rating per actor
    actor_rating = (
        actors
        .groupby('Actors')['IMDB_Rating']
        .mean()
        .sort_values(ascending=False)
    )

    # Director Analysis
    # Compute average rating per director
    director_rating = (
        df
        .groupby('Director')['IMDB_Rating']
        .mean()
        .sort_values(ascending=False)
    )
    # Compute average gross per director
    director_gross = (
        df
        .groupby('Director')['Gross']
        .mean()
        .sort_values(ascending=False)
    )

    #Graph set up
    def plot_series(series, title, ylabel, top_n=None, fmt='%.0f'):
        if top_n:
            series = series.head(top_n)
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = series.plot(kind='bar', ax=ax)
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.set_xticklabels(series.index, rotation=45, ha='right')
        #display values above bars
        ax.bar_label(bars.containers[0], fmt=fmt, padding=3)
        plt.tight_layout()
        plt.show()

    #Create graphs
    plot_series(
        avg_votes,
        'Average Votes by Genre',
        'Average Votes',
        fmt='%.0f'
    )

    plot_series(
        avg_rating,
        'Average Rating by Genre',
        'Average Rating',
        fmt='%.2f'
    )

    plot_series(
        actor_counts,
        'Top 10 Actors by Movie Count',
        'Movie Count',
        top_n=10,
        fmt='%.0f'
    )

    plot_series(
        actor_rating,
        'Top 10 Actors by Average IMDB Rating',
        'Average Rating',
        top_n=10,
        fmt='%.2f'
    )

    plot_series(
        director_rating,
        'Top 10 Directors by Average Rating',
        'Average IMDB Rating',
        top_n=10,
        fmt='%.2f'
    )

    plot_series(
        director_gross,
        'Top 10 Directors by Average Gross',
        'Average Gross (USD)',
        top_n=10,
        fmt='%.0f'
    )

if __name__ == '__main__':
    main()
