

Cs50 Project Design

Aghyad Deeb

December 2021

1 Project design breakdown

I will discuss each function in the app.py ﬁle by order. Starting with the ”reg-

ister” function, I have chosen to put several ﬁelds and to make the website

exclusive to Harvard students by returning an error message if the email does

not end with ”@college.harvard.edu. The purpose of this is that students would

have more motivation to check the website frequently since all users have things

in common which is being Harvard students and living in the same area. I have

also chosen to add a class ﬁeld in order to make it more relatable. For example,

a lot of seniors have a thesis, and all freshmen share the excitement and anxiety

of being here for the ﬁrst time. The information the user entered is stored in a

database.

In order to verify that the user is actually a Harvard student, there is con-

ﬁrmation page. The user is sent a conﬁrmation code generated randomly from

uppercase characters by email. after entering the conﬁrmation code correctly,

the user is redirected to the homepage.

In the home page there is the text box to enter the code and the submit and

upload photo button. All the posts are stored in a list along with the username,

session id, class, photo, and the date of posting. I have chosen to store the

posts in a list because it is updated each day and there is no need for previous

posts to be saved. By default, there is a bunch of fake posts saved in the posts

array so the website wouldn’t be empty. In addition, with the same goal of the

website not being empty, the old posts are only deleted when a post is posted

in a diﬀerent date. Then, the website checks if the user has already posted this

day and returns an error message if so. If not and if the date is diﬀerent from

the date of the last post, the website would pick a random post from the posts

list and save the diﬀerent values that the post indicate in order to pass them

to ”home.html” later. After picking the post, the website clears the posts array

so the website doesn’t pick a post from the previous day in the following day.

Afterwards, the website saves the details of the post and adds it to the posts

array and redirects to the same homepage.

1





The allowed ﬁle function is used to store the image extensions so the user does

not upload ﬁles which are not images, and the upload image function handles

the image uploading process and returns errors for the possible unintended use

cases. I tried to implement the ﬁle uploading process using php originally but I

could not ﬁnd a way to implement php in ﬂask.

Finally, the login, logout, and errorhandler functions are the same functions

from the ﬁnance pset.

When it comes to the html ﬁles, I tried to keep he design clean and simple.

2

Youtube video link:
https://youtu.be/qspeN12Be7M
