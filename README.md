This software uses is made for use only on macOS and Linux distributions on the most recent version of Python (3.11.4 as of 8/6/2023). If you use an older version of Linux it will not be nearly as accurate, for deployment in answering questions (they cannot have the most recent version of Python. It is also recommended not to use Replit as it uses an Ubuntu version of Linux that is 2 versions behind, and uses an older version of Python. Replit should be fine for demo purposes though and if you are just using this for personal use and nothing more.

to install the required libraries first update Linux using the following commands

* sudo apt update
 
* sudo apt upgrade

- When asked a for validation input y then enter

afterwards check for python being installed on the system with:

* python3 –version


Then install the requirements via the requirements.txt file which will run with python:

* pip install -r requirements.txt 


When the program runs in this demo it will ask you for your question and will scan all of the scraped web pages for the answer and will NOT make up an answer unless it lies within the context provided from the scraped documents. This means that if you ask it a question that is never touched in the documents provided it will not answer it.

It uses langchains to run and get the prompt. It will also display the source(s) of it’s information to the screen after providing an answer based on at least four sources from the scraped information.

*note* 
The scraped data is raw data but is efficiently stored and displayed to the user by the chatGPT API so even though raw website data is scraped including some HTML data this doesn’t have a large storage determent, or any effect on the user.

UPDATING DATABASE___________________________________________________________

While creating I figured that updating the database would likely not be a daily occurrence, to make it cheaper for the user (chatGPT API cost a lot of money if updating regularly) I made it so that to update the database for any reason the user must first delete the current database within the application folder. Before doing this however it is good practice to back up the current database first to do this back up the following:

* CheatSheets
* db

Back up these folders on a separate drive then delete them so that only the main.py, README.md, and requirements.txt file remain. The program will automatically re-create the database by scraping the entire website of all of it’s cheat sheets and then saving it to a chromaDB database. Doing this will take up to one minute and the code will let you know when it finishes via the terminal. After it finishes you will be able to type in a question.

This code will detect if a new cheat sheet is added, deleted or updated but only after an update of the database in the paragraph above. 

Please if you want a previous version of the database for any reason just put the older backup versions of CheatSheets folder and db folder in the old location and replace the newer/non-existent versions.



P.S.

PLEASE READ

For you to run this code you must have your own API key for chatGPT I will be deleting mine shortly after receiving payment. They cost around 20$ a month but can go up a lot if it automatically updates on it’s own and can cause slower experiences for the user especially if you aren’t updating the website quite regularly (which is why I didn’t do that). 

Add your key by going to line 84 in the code which looks like this:

os.environ['OPENAI_API_KEY'] = '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'

and update the part after the “=” asign with your code but keep the single quotes ‘’ around the API key it’self.

If you want me to update the code to make it update the Chromadb database over a period of time I can do that. But it won’t add much utility and will likely just cost you more money than it’s worth. I would recommend updating the database with the above instructions after making updates to the website itself. Using chatGPT from the user end of this program is not that expensive but updating the database automatically definitely can be.

Also it uses the Glossary to quickly scrape the data off of every cheatsheet. If you significantly change this part of the website the code might not function as intended.

Sorry for the wordy explanations, but hopefully you’re as satisfied with the work as I was while making it. :)
