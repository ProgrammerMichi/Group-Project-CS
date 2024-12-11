from APIConnection import Instance
import streamlit as st

#This function takes all input from the main page and, depending on whether they should be included, 
#adds them to a dictionary, which is used by the tmdbv3api to get the selected information

#ChatGPT helped with idea of using an empty dictionary

def findmovie(selgen, actor_check, selactor, keyword_check, selkeywords, excl_check, exclkeywords, selorder, rating_check, 
              selmin_rating, selmax_rating, selmin_votes, selmin_length, selmax_length, length_check):
    search_parameters = {}
    if selgen != "None":
            search_parameters["with_genres"] = str(Instance.get_genre_id(selgen))
    
    if actor_check and selactor:
        try: 
            selactor_id = Instance.person.search(selactor + " ")
            search_parameters["with_cast"] = str(selactor_id[0].id)
        except: 
            st.write("**Actor not Included in Search**:")
            st.write("Actor not found, please adjust actor names")
        
        else:
            selactor_id = Instance.person.search(selactor + " ")
            search_parameters["with_cast"] = str(selactor_id[0].id)

    if keyword_check and selkeywords:
        try:
            search_parameters["with_keywords"] = str(Instance.get_keyword_id(selkeywords))

        except:
            st.write("**Keywords not implemented in search**:")
            st.write("Please only use one keyword. If you have already entered only one keyword, try changing it.")

        else:
            search_parameters["with_keywords"] = str(Instance.get_keyword_id(selkeywords))


    if excl_check and exclkeywords:
        try:
            search_parameters["without_keywords"] = str(Instance.get_keyword_id(exclkeywords))

        except:
            st.write("False Use of Keywords:")
            st.write("Please only use one Keyword, if you have already entered only one Keyword, try changing it.")

        else:
            search_parameters["without_keywords"] = str(Instance.get_keyword_id(exclkeywords))
    
    if selorder == "Descending":
        search_parameters["sort_by"] = "vote_average.desc"
    else:
        search_parameters["sort_by"] = "vote_average.asc"
    
    if rating_check:
        search_parameters["vote_average.gte"] = str(selmin_rating)
        search_parameters["vote_average.lte"] = str(selmax_rating)
        search_parameters["vote_count.gte"] = str(selmin_votes)

    if length_check:
        search_parameters["with_runtime.gte"] = str(selmin_length)
        search_parameters["with_runtime.lte"] = str(selmax_length)


    moviesfound = Instance.discover.discover_movies(search_parameters)

    return moviesfound
