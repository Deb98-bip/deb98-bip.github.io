# INSTASHIELD
#### Video Demo:  <https://youtu.be/CmtVTXjQw20>
#### Description:

**Introduction**
InstaShield is a web application that allows users to automatically delete unwanted comments from their Instagram posts.

**Usage**
After loggin in with their Instragram account credentials, the users will directed to the home page. An error message will appear if the username and/or password are wrong.
On the home page, users are able to add and remove words or complete sentences to a list. They also have the option to make the screening of specific inputs case sensitive and they can decide to screen all or just some Instagram posts. Once the delete button is clicked, the selected words/sentences will be deleted from the Instagram comments of the selected posts. An error message will appear if no words were selected or if there are double inputs. The comment will be deleted only if it is a full string match with the user input. For example if the user input is "red" and a comment says "I love *red*dit" the comment will not be deleted. Once the screening is complete and all unwanted comments have been deleted, the user will be directed to a "success" page. From there, the user can decide either to log out or go back to the home page. A navigation bar fixed at the top of the screen also allows the user to log out or go back to the home page at any time. The program uses Instagrapi to connect to the users Instagram account and retrive data such as posts and comments. Since it takes an average of oen minute for the API to respond, a loading page is rendered after the login and the delete post requests are returned.

**Programming languages**

The programming languages used in instashield are: Python for the backend, Flask, html, css, javascript and jinja for the frontend.

The Instagrapi API rapresents the core of this project. It allows though Python to connect to a user's Instagram account, retrieve information such as media and comment count, as well as comment text all of which can be see in the app.py file, more specifically in the "/" (login) and "/delete" routes.

Once the user logs in to their Instagram account, both their user ID and their username are saved into Flask's session dictionary. This is how the "/" route eventually communicates its information to the  "/delete" route. As you might have noticed, no database such as SQL was created for this project. There are two main reasons for this. First I didn't want to register user's Instagram credential into a database for security reasons, as my computer might be subject to hacker attacks and I do not yet detain the skills to fully protect my programs against these types of hazards. Secondly, the Python backend was my main focus through this project. Implementing a database would have required extra front end developement such as a registration page which was not my top priority.

Once the user gets to the "/ban" route a Flask session is creted to store the list of undesired alphnumerical strings that user inputs. Another session records through boolean vaiables if a string is case sensitive or not. these two lists are combined together through a zip function in a third new list which is then returned through jinjja to render the ban.html table template. This is how the case sentitive icon in the table can be displayed and this will also determine if the original comment text should be upper case in the "/delete" route.

Trough the  "/ban" route, users can delete strings they sumbitted to their list without any errors or interruption to their user experiense. Thanks to jinja the html table will dynamincally resize to reflect the current list.

After the user access the "/delete" route through the post method, the screening process begins. First off, according to the value submitted in the form, the algotithm determines how many "medias" (ie. Instagram posts) are screened. The default value in the form is all, in this case the variable is set equal to the lenght of lists of disctioanries of medias. If not, the varible is set to the number specified by the user and the screening will be done that determined number of times starting from the last post. If the users enters an excessive value by mistake (let's say they users only has 3 posts but accidentally submitted to screen the last 50 posts), no error message will not be renedered, instead the program will simply screen through all posts.
Once the actual screening process begins, it is important that only comments containing the string sumbitted ending in null are deleted. To do this I used a python library called re with it's "findall" module that allows to divide a larger string in a list of it's substrings by ignoring non alphanumeric caracters. In this way, even comments that only contain one hashtag for example #red can be elegible for the screening. However, the downside to this is that a non alphanumeric string cannot be deleted from the comments.

Next, as it's iterating trough the list of "banned strings", the program determines if the iteam in the list is a single word or sentence. If if it's a single word then is can simpley compare the string to the stripped comment text (done with findall). If it's a sentence it first needs to find this sentence in the un-stripped comment text and it then needs to compare the banned string to the comment text making sure they match word per word starting with wherever the banned string appears in the comment string. In this case a comment saying "I love reddit" will not be deleted if the banned string was "I love red".
In case a match is found, the entire comment with all its replies will be deleted through the comment_bulk_delete method in the Instrgrapi.

As far as error handling is concerned, there are 4 possible errors:
If wrong password or username is submitted (this is the template for any 500 error that has not been accounted for in the code)
If  an empty string is submitted to the list
If a string cointaining nonalphanumeric characters (not including spaces) si added to the list
If a string aleardy present in the list is added

**Potential improvements**
Instagram does not like "bots" not even when they are meant to imporve user's mental health like InstaShield is meant to do.
For this reason my IP got blocked by Instagram multiple times. Instagrapi suggests to use a better quality proxy, that is something I might consider doing in the future.

**Inspiration**
The inspiration for this project came from hearing an increasing amount of Instagram users (influencers specifically) complaining about the high toxicity of the comment sections. It suffice to skim over the comments under the posts of some public figures to confirm this. Instagrams' algorithm only blocks comments that contain profanity or straighforward offenses. Most toxic or mean comments are more subtle and therefore can escape the algorithm. With InstaShield I wanted to possibly create the opportunity for people to delete any comments that they might find offensive, annoying or simply uninteresting (however subjective that may be) without having to reading them first. It is their account after all and they should be able to manage it as they prefer.

**Conclusion**
I enourmously enjoyed working on this final project and the CS50 experience overall. I am looking forward to scaling up InstaShiled and hopefully bring it public one day.
