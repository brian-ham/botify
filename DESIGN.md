Overall Design
-----------------------------------
The website was designed to be as minimalistic and lightweight as possible while still containing all the necessary components; the goal was that any user could input a text and receive their playlist in under a minute with minimal hassle.

The homepage contains the website "logo" as well as a button that takes users to the "Get Started" page, which contains a form for users to fill out. The first input takes in a text, which the users can copy and paste from an external file. The form also takes into account a couple of other factors, danceability and energy, which help narrow down the search for songs that fit a person's mood. Submitting the form takes people to the Results page, where users can see the songs of the resulting playlist.

Process Overview
-----------------------------------
How does the website know which songs pertain to a certain text? My project used elementary natural language processing (NLP) to map Spotify songs to a block of text. First, using the Spacy library, my program tokenized and extracted the keywords from the inputted text (a method logically named "keyword extraction.") Prior to this, the entire text had to be turned lowercase in order to be fully case-insensitive Following this each keyword was "lemmatized," or reverted back to their root form; for example, "apples" would become "apple," while "studies" would become "study." By referring to each keyword by the lemmatized form, this reduced the number of keywords that the program had to account for as it no longer had to consider variations of words. Lemmatization was used instead of stemming as stemming, while faster, is not always entirely accurate in reverting words to their root forms. The lemmatized keywords were returned to the program as a list.

While the process above extracted the keywords of the text, we still need a way to characterize each song. One such method could be extracting keywords from song titles, but this would not always be accurate as not only are they sometimes irrelevant to the actual lyrics, but the sample size would be too small to get an accurate keyword list. Instead, I turned to the specific musical key that each song was written in: for exmaple, Lady Gaga's "Bad Romance" is written in A minor, while "Bohemian Rhapsody" is a B flat major. There are a total of 24 musical keys: a major and minor key for each of the 12 chromatic notes (C, C#, D, D#, E, E#, etc.). Each key tends to have a different "feel" to them, and in 1713, German music theorist and composer John Mattheson made this concrete by describing each musical key and what emotions they evoked for him. A C major felt like the the innocence of children, while a B flat major spelled pessimism and a "belief in darkness." The database I used contained the top 10,000 songs of the past two years as well as the keys they were written in, stored in two variables "key" and "mode," meaning this information was easily accessible. I turned John Mattheson's descriptions into a series of keywords and stored it in a list of sets in app.py.

Now, we have a list of keywords for the text and a list of keywords for each musical key; now, app.py logically compared the two and selected the musical key that most closely matched the keywords of the text. Finally, a SQL query selected roughly 20 songs from the database that were written in that key. For extra customization, this query also accounted for the "danceability" and "energy" or songs; these were two characteristics that were quantified in the database I used as a decimal from 0 to 1. The query selected a random set of 20 songs so that users could reload the page and get an entirely fresh playlist.

Code Overview
-----------------------------------

To code this page, I used Flask and Jinja to dynamically render the templates necessary. The app.py file was designed as follows:

1) Relevant libaries were imported.
2) Databases and dictionaries necessary for NLP were loaded.
3) "keys[]", a list of sets, was a global variable that contains words pertaining to each musical key, as mentioned above. These were inputted as sets so that lookup time would be constant and the program could handle large blocks of text.
4) The index and about functions only receive GET requests that display their corresponding pages.
5) "The getstarted" page also takes a POST request when the form is submitted, and contains the Python code necessary to perform keyword extraction on the text and compare to the predetermined "keys," as well as return the relevant SQL query.

The CSS and HTML were designed to fit the Overall Design above: simplistic, but also aesthetic (by the standards of a prospective CS major who has little talent in actual artistic design.)

1) For the CSS, I used CSS transitions to infinitely loop the background between two gradients, creating a "pulsing" effect.
2) The font, Gotham Medium, was also specifically chosen to resemble Spotify.
3) The Bootstrap navbar allows users to navigate between the tabs.

Finally, the NLP processing function once included in a separate file, helpers.py, for better organization.

The Data page provides users some extra information about their playlist choices, by representing the average valence (positivity), popularity (as measured by Spotify users), and the average tempo (measured in beats per minute.)

Sources:

https://ledgernote.com/blog/interesting/musical-key-characteristics-emotions/
https://towardsdatascience.com/keyword-extraction-process-in-python-with-natural-language-processing-nlp-d769a9069d5c
https://www.analyticssteps.com/blogs/what-stemming-and-lemmatization-nlp
https://betterprogramming.pub/extract-keywords-using-spacy-in-python-4a8415478fbf
https://www.w3schools.com/css/css3_animations.asp
https://stackoverflow.com/questions/16989585/css-3-slide-in-from-left-transition