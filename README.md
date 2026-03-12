# Study Space
#### Video Demo:  https://www.youtube.com/watch?v=bEH_eHY5lT8
#### Description:
My project is a web based application aimed towards students to help them organise their school work and make their study experience easier by providing more convenience.

##### /static
in this folder contains images of emojis used to decorate the website, as well as a style.css file that serves as the style sheet for the website.

###### /templates
in this folder contains html files that formats the website.
/apology.html:
displays an image of a sad cat and text that decribes where the user has not filled in a particular input, or if the user's account is not found.
/forgor.html:
when the user clicks forget password, this leads the user to a page where they can confirm their name and username to check that they do have an account in the sql database of the website stored in final.db
/forgorconfirm:
leads the user to a page to change their password after confirming that their account does exist in the database, and then brings them to he home page directly
/index.html:
displays their name, todays date, their to do list and their quick links list. in this page the user can add or delete rows of their to do list and the quick links list. the to do list can also create a line through the row when the user clicks on the row. the quick links list will bring the user to the specified url by clicking on the name they have assigned to the url.
the todolist table rows all contain event listeners that triggers a toggle that makes a lone through the text of the row. i thought of just directly deleting the row right away, but as a student it feels more satisfying to see what i have done so far before finally deleting the rows at the end of the day. in the end i only put a line through display which makes it more similar to a checklist.
/layout.html:
this is the main layout of the websit ethat is applied to all html files. this contains the navigator bar that allows the user to access different parts of the website.
i thought about creating a seperate page for editing the tables, but it would look almost exactly the same as the index() page, or it would be inconvenient for the user to not see the data they already have in the home page.
in the end i created a pop up window instead. this pop up appears when the user clicks on the edit button, which makes for a smoother user experience.
/login.html:
this is the login page of the website where the user can input their username and password. it also has a forget password button to let the user change their password. this is also the main page of the website.
/register.html:
this is the register page where users can register by inputting their own name, username and password.

##### apology.py
this contains python code for the app route of apology.html and @login_required

##### app.py
this contains the main python code for the website
index()
name: gets name of user from sql database
links: gets link_id, name, and url from links table in sql
todolist: gets data from todolist table, calculates the number of days left between todays date and the deadline.
todolistadd()
takes user input and adds new data into todolist table
deleteactivityrow()
takes activity_id and deletes row of data from todolist table
at first i debated whether to just hide the row instead of passing data back to python to be able to delete it from the sql database, but the index() would still display it, hence it would be better to forget unwanted data to keep track of the important data.
linksadd()
takes user input and adds new data into links table
deletelink()
takes link_id and deletes row of data from links table
login()
logs user in, checks is username and password input are filled. checks database for user
forgor()
checks if user already exists
forgorconfirm()
changes password of user account
logout()
logs user out
register()
takes users name, username and password to create a new account

final.db
this is a sql file that contains three tables, user, todolist and links
user table stores user id, name, username and hash of the user's password
todolist stores activity_id, user id, task, deadline and days left
links table stores link_id, user id, name of url, and url
