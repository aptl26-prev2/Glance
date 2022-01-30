Aghyad Deeb

December 2021

1 Motivation and general descrition

My CS50 ﬁnal project is Glance, a social media network for Harvard students

which is a bit diﬀerent. Glance is based on the idea of uniqueness, in social

media networks like Facebook, Instagram, and Twitter, one can post as many

times as they desire, which may result in the posts not being valuable since

one can always post without any limits. However, in Glance, one can only post

once per day. In addition, each day there is a general theme displayed in the

homepage for users to follow in there posts. The cherry on top is that each

day, there is one post that is randomly chosen and pinned to the top of the

homepage, therefore this post is seen by all users adding more potential value

to user’s posts.

2 How to use Glance
First open the file after cloning it and then open terminal in the file and type

 $ flask run
 
Afterwards, the user should ﬁrst register a new account by entering their

username, a Harvard College email, class, and password with conﬁrmation. Af-

ter entering the required ﬁelds, Glance will automatically send an email to the

user’s email address containing a conﬁrmation code that the user should copy

and paste it in Glance. If the code is correct the website will allow the user to

proceed and redirect them to the homepage, otherwise the user will be told that

the code is incorrect. As mentioned earlier, the homepage contains the theme

of the day, in addition to the pinned post and other posts beneath. Moreover,

the homepage contains a space to post a new post and add a photo. In order

to post the user should enter the text they want to post and click submit. The

website will return an error message in case the user tries to post twice. In case

the user wants to add a photo to their post, they should click the ”Add photo”

button after submitting their post. The website will then redirect them to the

uploading page and the user can chose the photo they want to include and click

upload photo and their photo will be added to the post. Afterwards, the user

can press the ”return to homepage button” to continue exploring other users’

posts. Note that the pinned post is picked from the previous day’s posts but

other posts are the posts posted on the same day.
