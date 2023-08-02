import os
import re

from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_session import Session
from helpers import login_required

#https://adw0rd.github.io/instagrapi/
from instagrapi import Client

# Configure application
app = Flask(__name__)

cl = Client()

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#if wrong username or password (or if unaccounted 500 error)
@app.errorhandler(500)
def internal_error(error):
     return render_template('500.html'), 500

@app.route('/500')
def error500():
     abort(500)

#login route
@app.route("/", methods=["GET", "POST"])
def login():

    #clear session of all variables including ban list
    session.clear()

    if request.method == "POST":

        #retrive user account
        user_name = request.form.get("username")
        password = request.form.get("password")
        cl.login(user_name,password)
        user_id = cl.user_id_from_username(user_name)
        session["user_id"] = user_id
        session["username"] = request.form.get("username")

        return render_template("ban.html")

    else:
        return render_template("index.html")

@app.route("/ban", methods=["GET", "POST"])
@login_required
def ban():

    if request.method == "POST":

        #return error if empty added words
        if request.form.get("word") == "":
            session["words_case"] = zip(session["words"],session["case"])
            return render_template("empty.html")

        #return error if empty added words
        if not all(c.isalnum() or c.isspace() for c in request.form.get("word")):
            session["words_case"] = zip(session["words"],session["case"])
            return render_template("alpha.html")

        #return error if word already in list
        if "words" in session:
            if request.form.get("word") in session["words"]:
                session["words_case"] = zip(session["words"],session["case"])
                return render_template("double.html",word=request.form.get("word"))

        #responding to case sensitive request
        word = request.form.get("word")

        if request.form.get("case") == "not_upper":
            case = True
        else:
            case = False

        #add word to session list
        if "case" in session:
            session["case"].extend([case])
        else:
            session["case"] = [case]

        if "words" in session:
            session["words"].extend([word])
        else:
            session["words"] = [word]
        #join word list with case sensitive list
        session["words_case"] = zip(session["words"],session["case"])

        return render_template("ban.html")

    else:
        #need next line otherwise html table will not appear
        session["words_case"] = zip(session["words"],session["case"])
        return render_template("ban.html")

#remove words from list before deleting them from comments
@app.route("/remove", methods=["POST"])
@login_required
def remove():

    delete_word = request.form.get("delete_word")
    #need to delete word and case sensitive varible as well
    index = session["words"].index(delete_word)
    session["words"].remove(delete_word)
    session["case"].pop(index)
    session["words_case"] = zip(session["words"],session["case"])
    return render_template("ban.html")

#delete comments, medias is a term for posts
@app.route("/delete", methods=["POST"])
@login_required
def delete():
            #return error if user hasn't enetered any word
            if "words" not in session:
                return render_template("empty.html")

            #create list of all user medias
            l = cl.user_medias_v1(session["user_id"])
            if request.form.get("medias") == None:
                m = len(l)
            else:
                m = int(request.form.get("medias"))
                if m > len(l):
                    m = len(l)

            #custom number of posts to retrieve
            medias = []
            for n in range(m):
                user_media = cl.user_medias(session["user_id"], amount=m)[n].dict()

                media_pk = user_media["pk"]
                media_id = cl.media_id(media_pk)
                media = {"media_pk": media_pk, "media_id":media_id}
                medias.append(media)


            #run through all comments
            for media in medias:
                media_info = cl.media_info(media["media_pk"]).dict()
                comment_c = media_info["comment_count"]

                comment_pks = []
                comments = cl.media_comments(media["media_id"])
                for i in range(comment_c):
                    comment = comments[i].dict()
                    comment_pk = comment["pk"]

                    #responding to case sensitive request
                    for word, case in zip(session["words"], session["case"]):
                        if case == False:
                            word = word.upper()
                            comment_text = comment["text"].upper()
                            comment_text_stripped = re.findall(r'\w+',comment["text"].upper())
                            word_stripped = re.findall(r'\w+',word.upper())
                        else:
                            comment_text_stripped = re.findall(r'\w+',comment["text"])
                            word_stripped = re.findall(r'\w+',word)

                        if len(word_stripped) == 1:
                            if word in comment_text_stripped:
                                comment_pks.append(comment_pk)
                        else:
                            if word in comment_text:
                                if word_stripped[len(word_stripped)-1] == comment_text_stripped[comment_text_stripped.index(word_stripped[0])+(len(word_stripped)-1)]:
                                    comment_pks.append(comment_pk)
                #delete comment and/or continue to next post
                if not comment_pks:
                    continue
                else:
                    cl.comment_bulk_delete(media["media_id"], comment_pks)

            return render_template("success.html")





