# Overview

I feel like in today's world there is a lot of people who need employees who can perform quick and accurate data analysis. Data analysis can benefit almost every industry out there. In this assignment I wanted to test out data analysis and see if it was something that I am interested in. I found a database that included a bunch of data from the top 1000 movies on IMDb. I downloaded this database to and began thinking of questions that I could answer that could be useful for someone making a movie. These are the questions I cam up with: "Which genre attracts the most votes (as a proxy for popularity)?", "Which genre scores the highest ratings?", "Which actors star in the most films and earn the best average ratings?", "Which directors deliver the highest-rated and highest-grossing movies?" With these questions in mind, I feel it could help a company decide the genre of their film as well as popular actors/directors they could hire. This was a fun set to work with and there are so many interesting questions that can be answered. I began this project wanting to figure out if data analysis was something that I would be interested in doing and it is safe to say that it is.

Movie Database: https://www.kaggle.com/datasets/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows 

[Software Demo Video](https://youtu.be/3lZEZZNVsws?si=37TgiHTdKXVUuVvE)

# Data Analysis Results

Which genre attracts the most votes (as a proxy for popularity)?
The five genres the got the most votes was sci-fi (by far), adventure, action, fantasy, and thriller. They didn't have views availalbe for the movies in this dataset so using the votes was the next best thing I could think of.

Which genre scores the highest ratings?
The top five genres with the highest ratings are war, western, film-noir, sci-fi, and mystery. These are all very close going down by an average rating of 0.01 with each genre in the top five.

Which actors star in the most films and earn the best average ratings?
The actors that starred in the most films are Robert De Niro, Tom Hanks, Al Pacino, Clint Eastwood, and Brad Pitt. The actors with the highest average film rating are Bob Gunton, William Sadler, Aaron Eckhard, Caroline Goodall, and John Travolta. These answers can be skewed if these actors have less films that they are in compared to other actors. It would be better to analyze datasets containing more of their movies to figure out the best actor to hire for a film. 

Which directors deliver the highest-rated and highest-grossing movies?
The top five directors are Frank Darabont, Lana Wachowski, Irvin Kershner, Masaki Kobayashi, Fernanddo Meirelles, George Lucas, Sudha Kongara, Thomas Kail, and Roberto Benigni. (A 6 way tie for 4th starts with Masaki Kobayashi). The top five directors by average gross (USD) are Anthony Russo, Gareth Edwards, J.J. Abrams, Josh Cooley, and Roger Allers. This can have the same issue as the actors analysis did where the set may contain less data for some directors than others.  

# Development Environment

The biggest tool that I used to complete this project was the IMBd Movie Database. 

Progamming Language: Python
Libraries: Pandas, Matplotlib

# Useful Websites

* [Kaggle Datasets](https://www.kaggle.com/datasets)
* [Kaggle Pandas Tutoriol](https://www.kaggle.com/code/kashnitsky/topic-1-exploratory-data-analysis-with-pandas)
* [W3 Schools](https://www.w3schools.com/python/matplotlib_intro.asp)

# Future Work

* Include more in depth analysis for actors and directors
* Clean up graphs/more visually appealing
* Incorporate more movie datasets to get more accurate results