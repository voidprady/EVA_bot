# EVA_bot
#EVA is made to save us from the endless scrolling through streaming websites. 
#She can recommend movies based on genres, actors, directors and also search movie data based on the title.

# SET UP:
  #install rasa x. docs here -->(https://rasa.com/docs/rasa/installation) 
  #clone the repository
  #Go to the project directory and run "rasa train". This will take sometime as the bot is in training
  #once training is done. run "rasa shell" to talk to EVA.

#EVA uses imdb and rotten tomatoes csv file which is larger in size. so the db folder is compressed. before running the project please make sure you extracted the db folder in the project directory
#EVA is built using RASA Open Source using Python. She is still new and learning faster. Here are some basic conversation flows that you might be interested to try

#Conversation Flow 1 :

-> input: Hi
-> EVA: Hi! I am EVA, and I am here to help you pick a movie. You can ask me for movies based on genres, actors and directors. What can I assist you with today?
-> input: what is the day like
-> EVA :  It's a good day to watch a movie!
-> input : I wanna watch a movie
-> EVA : Sure! what kind of movie are you looking for ?
-> input : what has Tom Cruise starred in
-> EVA : Sit back while I crunch the numbers for you
-> EVA : you mean, tom cruise, right ?
-> input : yes
-> EVA : on it. The results should be up in a few seconds
-> EVA : Tom Cruise acted the following films: All the Right Moves, Losin' it, Risky Business, Legend
-> EVA: what are we looking up next ? 
-> input : that is all
-> EVA : cool, don't hesitate to reach back out to me.
-> Hope to see you again

#Conversation Flow 2 :
-> input: Hi
-> EVA: Hi! I am EVA, and I am here to help you pick a movie. You can ask me for movies based on genres, actors and directors. What can I assist you with today?
-> input: how is it going
-> EVA :  It's a good day to watch a movie!
-> input : I wanna watch a movie
-> EVA : Sure! what kind of movie are you looking for ?
-> input :find movies by Steven Spielberg
-> EVA : Sit back while I crunch the numbers for you
-> EVA : you mean, steven spielberg, right ?
-> input : yes
-> EVA : on it. The results should be up in a few seconds
-> EVA : Steven Spielberg directed the following films: Firelight, The Sugarland Express, Jaws, Close, Encounters Of The Third Kind
-> EVA: what else can i help you find? 
-> input : that is all
-> EVA : cool, don't hesitate to reach back out to me.
-> Hope to see you again

#Conversation Flow 3 :
-> input: Hi
-> EVA: Hi! I am EVA, and I am here to help you pick a movie. You can ask me for movies based on genres, actors and directors. What can I assist you with today?
-> input: how is it going
-> EVA :  It's a good day to watch a movie!
-> input : I wanna watch a movie
-> EVA : Sure! what kind of movie are you looking for ?
-> input :how about sci-fi movies
-> EVA : Sit back while I crunch the numbers for you
-> EVA : Let me see what I can find for you
-> EVA : sci-fi movie coming right up.
-> EVA : Here is my recommendation: The Day Mars Invaded Earth
-> EVA : Did that help you?
-> input : yes
-> EVA: what else can i help you find? 
-> input : that is all
-> EVA : cool, don't hesitate to reach back out to me.
-> Hope to see you again

#Conversation Flow 4 :
-> input: Hi
-> EVA: Hi! I am EVA, and I am here to help you pick a movie. You can ask me for movies based on genres, actors and directors. What can I assist you with today?
-> input: how is it going
-> EVA :  It's a good day to watch a movie!
-> input : I wanna watch a movie
-> EVA : Sure! what kind of movie are you looking for ?
-> input :how about sci-fi movies
-> EVA : Sit back while I crunch the numbers for you
-> EVA : Let me see what I can find for you
-> EVA : sci-fi movie coming right up.
-> EVA : Here is my recommendation: The Day Mars Invaded Earth
-> EVA : Did that help you?
-> input : nope
-> EVA : I got something just for you.
-> EVA : sci-fi movie coming right up.
-> EVA : Here is my recommendation: The Lost City
-> EVA : Did that help you?
-> EVA : yes
-> EVA: what else can i help you find? 
-> input : that is all
-> EVA : cool, don't hesitate to reach back out to me.
-> Hope to see you again

# Conversation flows can be extended to ask further questions like showed in the examples below.
![alt text](./sample%20conversation%20flows/flow_actor_extended.png)

#example extended conversation flow 2 :
![alt text](./sample%20conversation%20flows/flow_1.png)
