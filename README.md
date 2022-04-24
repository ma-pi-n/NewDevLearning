# Shortn - URL Shortener
## Video Demo [shortn demo](https://youtu.be/aMMG3uoTdR0)
## Description
Shortn is a URL shortener like [bit.ly](https://bitly.com/pages/landing/url-shortener). Shortn is walled with a simple user authentication. Users can register with username and password, and can login into the app with previously registered credentials.

Shortn allows logged in users to create a shortened url, update where the shortened url points to, view details about the url, view all shortened urls by the logged in user, delete urls and importantly, redirects user to the corresponding original long url that was shortened.

### User Flows 🤽‍♀️♒🌊

- **Home page:** This is the root page of the app. For an authenticated user, they get redirected to `/urls`, where they have all of their shortened urls. However, for an unauthenticated alien, they are redirected to the `/login` page.

- **Login page:** This page is sort of the home page for unauthenticated alien. An error is shown when the provided `username` and `password` does not match any user's record in Shortn's database. From this page, alien can choose to register instead of logging in.

- **Register page:** The `/register` page looks very similar to the login page, except that it registers a new user to Shortn. Once registration is complete, user will be automagically 🧙‍♂️🧙🪄 logged in to Shortn.

- **Urls page:** Once logged in, you are welcomed to Shortn on the `/urls` page. The unique purpose of this page is to list all previously shortened urls by the user. If the user hasn't shortened any urls, they are advised to do so by clicking the *shorten new link* button. The list of all urls is presented in a sort of tabular format. Each row has four interesting cells - the shortened link, the original link, an edit button and a delete button. Clicking on the shortened link takes user to the corresponding long url, while clicking on the usually truncated original link will open up the shortened url's details page. The edit button also links to the url's details page while the delete button, deletes the shortened url record.

- **New url page:** Clicking on any variations of 'shorten new' buttons will open up this `/urls/new` page, where long gargantuan urls are *shortnd*. After shortening is done, users are redirected to the *Urls page*, where the newly minted shortened url is now listed in a quasi-tabular format.

- **Url details page:** Perhaps the most complex page to build. This page shows the details of a shortened url with some analytics of how many people (visitors) have clicked on the shortened url and how many times.


---

## Nerdy Details 🤓🔬🛠️
This section includes technical details about how this project is put together and how one might run this web application locally.

### Project Structure
There are broadly five categories of files in this project. These categories are discussed below:


#### CSS 😊😁💅
Styling for this app is all included in one stylesheet - `static/styles.css`. This file is *link*ed in the header of all pages through the HTML templates. Also, worthy of mention is the fact that this project uses [Bootstrap 3.3](https://getbootstrap.com/docs/3.3/) to get some out of the box goodliness.


#### HTML Templates
HTML templates are the cornerstones of what the users see. They are used to structure contents semantically. In this project, all HTML templates are stored in the `/templates/` directory. Of note, is `template/base.html`, this file is where all other templates inherit from. This enables our templates to be DRY.


#### App.py
This is the entry point of the whole application. This file pulls together all the other files (except from README.md) in this project. The contents of this file could be logically divided into four parts. The topmost part includes imports from external libraries. Next section includes typical Flask app configurations.

The third section in this file is titled *BUSINESS LOGIC*. This includes helper functions that wraps core business logics and how to interact with the underlining database.

The last section contains Flask route handlers in all their glory. These handlers are responsible to receive and respond to all incoming requests. To respond to requests, these handlers leverage the business logic helper functions and decides whether to *render* a template or *redirect* to a different route.


#### Database file
The database file `urls.db` was an export from *phpLiteAdmin* sqlite GUI. This project used the sqlite GUI to create the needed tables within its database; namely `users`, `urls` and `visits`.

The `users` table stores users information including the `username`, `password` and an auto-generated `id` as the primary key.

The `urls` table is where data about shortened urls are stored. It's schema includes an externally generated random string as `id`; this is the primary key on this table. Other columns are the `long` column that stores the user inputted long url and the `user_id` column, which is a *foreign key* to the `users` table, representing the logged in user who created this particular shortened url row of record.

Lastly, the `visits` table stores the analytics about how many times a particular shortened url has been visited. It also tracks by which unique visitor. The logic of how this works is in `log_visit` helper function within `app.py` - this relies on Flask sessions and cookies.


#### Readme.md 📖🧾📚
This README file you've been reading so far attempts to document details about the whole project altogether. Hope you've enjoyed reading it ;)


### Running the app locally 💨🏃‍♀️🏃
To run this app locally, make sure you have the following installed:

- **Python 3** - as appropriate for your operating system
- **flask** - installed with `pip`. For example: `pip install flask`
- **cs50** - also installed with `pip`. For example `pip3 install cs50`

Once all those are installed, run `python -m flask run` to run the app. If all the stars align, the app should be live on [http://127.0.0.1:5000](http://127.0.0.1:5000)



Made with 💜💌💜 by yours truly; Jelilat Adebayo. Peace ✌️🕊️✌️
