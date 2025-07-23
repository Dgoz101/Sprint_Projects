# Overview

I wanted to stretch myself with a real web framework and build something I’d actually use. I cook a lot and I’m always digging through random 
notes or screenshots for recipes, so I decided to make a recipe collection site. Django was a tool that was recommended to me to get hands-on with 
models, forms, file uploads, and templating. The app lets me browse recipes, open a detailed view with ingredients and steps, and submit my own 
recipes (with photos). I also added comments and a star rating system because feedback is half the fun. Eventually I'd like to add user accounts 
so that comments and recipes are tied to actual people/users. I also challenged myself to leave more comments so that others can follow along the 
code better.

To run it locally:

```bash
# from the folder with manage.py
python manage.py migrate     # set up the database
python manage.py runserver   # start Django's dev server
````

Then open **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser.

[Software Demo Video]()

---

# Web Pages

### Recipe List (`/`)

This is the landing page. It pulls all recipes from the database and shows them as cards (thumbnail, name, and average rating). I added a little scroll animation so cards fade up as you scroll.

### Recipe Detail (`/recipe/<id>/`)

Clicking a card drops you onto the detail page. You’ll see the full recipe info: photo, description, ingredients, and ordered steps. Users can leave comments and rate the recipe with a star widget. Submitting a rating recalculates the average immediately. Sections fade in as you scroll for a cleaner feel.

### Add Recipe (`/add/`)

This page has a multipart form for uploading an image plus all the fields for the recipe. I wired up “Add another” buttons with JavaScript so you can keep adding ingredients or steps without refreshing the page.

**Extras:**

* Dark mode toggle (saved in `localStorage`).
* Responsive nav with a hamburger menu on small screens.
* Smooth page transitions when navigating around the site.

---

# Development Environment

- **Tools:** VS Code, Git, Pillow (for image uploads)
- **Language/Framework:** Python 3.x, Django
- **Frontend:** Vanilla CSS and JavaScript (custom theme, IntersectionObserver animations)

---

# Useful Websites

* [Django Documentation](https://docs.djangoproject.com/)
* [Real Python – Django Tutorials](https://realpython.com/tutorials/django/)
* [MDN Web Docs – Forms](https://developer.mozilla.org/en-US/docs/Learn/Forms)
* [Django Formsets](https://docs.djangoproject.com/en/stable/topics/forms/formsets/)
* [W3C CSS Transitions](https://www.w3.org/TR/css-transitions-1/)

---

# Future Work

* Add edit/delete options for recipes, ingredients, steps, and comments
* Tie ratings/comments to logged-in users (auth)
* Add search and filtering by tags/cuisine/difficulty
* Prettier URLs with slugs instead of numeric IDs
* Expose a small API for mobile or other clients

