# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from actions import services as recommenderService

ratedMovies = recommenderService.imdb_movies

class ActionGetMovieByGenre(Action):

    def name(self) -> Text:
        return "action_get_movie_by_genre"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        genre_1 = next(tracker.get_latest_entity_values("genre", "genre_1"), None)
        genre_2 = next(tracker.get_latest_entity_values("genre", "genre_2"), None)
        genre_3 = next(tracker.get_latest_entity_values("genre", "genre_3"), None)
        
        genres = [genre_1, genre_2, genre_3]
        if(not genre_1 and not genre_2 and not genre_3):
            genre_1 = tracker.get_slot('genre_1')
            genre_2 = tracker.get_slot('genre_2')
            genre_3 = tracker.get_slot('genre_3')

            genres = [genre_1, genre_2, genre_3]
        genres = list(filter(None, genres))

        genres_str = ', '.join(map(str, genres))
        dispatcher.utter_message("{} movie coming right up.".format(genres_str))
        genre_movie_rec = tracker.get_slot('genre_movie_rec') or None
        recommendation = recommenderService.rec_movie_by_genre(genres, genre_movie_rec)
        dispatcher.utter_message("Here is my recommendation: {}".format(recommendation))

        return [SlotSet(key = "genre_movie_rec", value = recommendation), SlotSet(key="genre_1", value=genre_1), SlotSet(key="genre_2", value= genre_2), SlotSet(key="genre_3", value=genre_3)]

class ActionActorVerification(Action):

    def name(self) -> Text:
        return 'action_actor_verification'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        actor = tracker.get_slot('actor')
        suggested = recommenderService.is_this_your_person(actor)
        print("suggested", suggested, actor)
        if(len(suggested) == 0):
            dispatcher.utter_message("Sorry, Seems like there aren't any actors with that name.")
        else:
            latestIntent = tracker.get_intent_of_latest_message()
            bestmatch = suggested[0][0]
            if latestIntent == 'deny':
                if(len(suggested) > 2): 
                    bestmatch = suggested[1][0] 
                else: bestmatch = suggested[0][0]
                SlotSet("actor", bestmatch)
            else:
                bestmatch = suggested[0][0]
                SlotSet("actor", bestmatch)
            dispatcher.utter_message("You mean, {}, right?".format(bestmatch))
            suggested_movies = recommenderService.get_movies_by_actor(bestmatch)
            print("suggested_movies", suggested_movies)
            return [SlotSet("actor_movies", suggested_movies)]
        
        return []

class ActionGetMovieByActor(Action):
    
    def name(self) -> Text:
        return "action_get_movie_by_actor"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        actor = tracker.get_slot('actor')
        movies = tracker.get_slot("actor_movies") or None
        print("movies", movies)
        if movies:
            print("movies from slot", movies)
            dispatcher.utter_message("{} acted the following films: {}".format(actor, movies))
        else: 
            movies = recommenderService.get_movies_by_actor(actor.lower())
            print("movies", movies)
            dispatcher.utter_message("{} acted the following films: {}".format(actor.lower(), movies))
    
        return []

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []

class ActionmovieVerification(Action):

    def name(self) -> Text:
        return 'action_movie_verification'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        movie = tracker.get_slot('movie_title')
        print("movie", movie)
        suggested = recommenderService.is_this_your_movie(movie)
        latestIntent = tracker.get_intent_of_latest_message()
        if(len(suggested) > 0):
            if latestIntent == 'deny':
                if(len(suggested) > 2): 
                    bestmatch = suggested[1][0] 
                else: bestmatch = suggested[0][0]
                SlotSet("movie_title", bestmatch)
            else:
                bestmatch = suggested[0][0]
            dispatcher.utter_message("You mean, {}, right?".format(bestmatch))
        else:
            dispatcher.utter_message("Sorry, i don't find movies matching that name.")
        return []

class ActionSearchMovieData(Action):

    def name(self) -> Text:
        return "action_get_movie_data"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        movie_title = tracker.get_slot('movie_title')
        print("search movie", movie_title)
        suggested = recommenderService.is_this_your_movie(movie_title)
        bestmatchmovie = suggested[0][0]
        movie_df_len = recommenderService.get_number_of_titles(bestmatchmovie)
        intent = tracker.get_intent_of_latest_message()
        print("intent", intent, bestmatchmovie, movie_df_len)
        if intent == 'affirm':
            if movie_df_len == 1:
                movie = recommenderService.get_movie_data(bestmatchmovie)
                dispatcher.utter_message("Here is what I could find on {}".format(bestmatchmovie))
                dispatcher.utter_message(movie[0])
            else:
                result_other = recommenderService.get_movie_data(bestmatchmovie)
                dispatcher.utter_message("There are multiple movies by that name. "
                                         "Here are your choices to narrow it down:")
                for i in result_other:
                    dispatcher.utter_message(i)
        return []

class ActionDirectorVerification(Action):

    def name(self) -> Text:
        return 'action_director_verification'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        director = tracker.get_slot('director')
        SlotSet("director_movies", '')
        suggested = recommenderService.is_this_your_person(director)
        latestIntent = tracker.get_intent_of_latest_message()
        bestmatch = suggested[0][0]
        if latestIntent == 'deny':
            if(len(suggested) > 2): 
                bestmatch = suggested[1][0] 
            else: bestmatch = suggested[0][0]
            SlotSet("director", bestmatch)
        else:
            bestmatch = suggested[0][0]
        dispatcher.utter_message("You mean, {}, right?".format(bestmatch))
        rec_movies = recommenderService.find_movies_by_director(bestmatch)
        
        return [SlotSet("director_movies", rec_movies)]

class ActionSearchMovieDirector(Action):

    def name(self) -> Text:
        return "action_get_movie_by_director"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        director = tracker.get_slot('director')
        suggested = recommenderService.is_this_your_person(director)
        bestmatch = suggested[0][0]
        rec_movies = tracker.get_slot("director_movies")
        print("director_movies", rec_movies)
        if(rec_movies is None or len(rec_movies) == 0):
            rec_movies = recommenderService.find_movies_by_director(bestmatch)
        dispatcher.utter_message("{} directed the following films: {}".format(bestmatch, rec_movies))
        return []