import os
from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from dotenv import load_dotenv
from searchbooks import search_books, get_volume_id
from deepseekai import ask_ai, similar_book_ai
import json
import re
# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure database & Flask settings
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///capstone_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')

# Enable Debug Toolbar
toolbar = DebugToolbarExtension(app)

@app.before_request
def log_request():
    # Log incoming request details for debugging purposes
    app.logger.info(f"Request: {request.method} {request.url}")
    app.logger.info(f"Headers: {request.headers}")
    app.logger.info(f"IP: {request.remote_addr}")

@app.route('/RPC2', methods=["POST"])
def rpc2():
   
    return '', 204

######################################################################

@app.route('/')
def homepage():
    return redirect("/search")

@app.route('/search', methods=["GET", "POST"])
def search():
    """Fetch search results directs to Google Books API"""
    query = request.args.get("q")  
    books = []
    max_results = 6

    if query:
        books = search_books(query, max_results)  

    return render_template("home.html", books=books) 
@app.route('/bookpreview/<volume_id>')
def bookpreview(volume_id):
    """Fetch book details directly using Volume ID."""
    book = get_volume_id(volume_id)

    if not book:
        flash("Book preview unavailable.", "warning")
        return redirect("/search")

    return render_template("books.html", book=book)

@app.route('/ask_ai', methods=["GET", "POST"])
def ask():
    """Test the AI """
    if request.method == "POST":
        user_question = request.form.get("question") 
        response = ask_ai(user_question)  

      
        ai_answer = response.get("choices", [{}])[0].get("message", {}).get("content", "No response.")
        
        return render_template("testAi.html", question=user_question, answer=ai_answer)

    return render_template("testAi.html", question=None, answer=None)

from flask import flash, redirect, render_template

@app.route('/bookrecommendation/<volume_id>', methods=["GET", "POST"])
def bookrecommendation(volume_id):
    """Fetch AI book recommendations and find similar books."""
    book = get_volume_id(volume_id)
    if not book:
        return redirect(f"/bookpreview/{volume_id}")

    # Get AI recommendations by calling /bookaifetch/<volume_id>
    ai_response = similar_book_ai(book)

    if "error" in ai_response:
        flash("AI Response Error: {}".format(ai_response["error"]), "error")
        return redirect(f"/bookpreview/{volume_id}")

    recommended_book_names = list(ai_response.values())  # Get only book titles

   
    simbooks = []

    max_results = 1  # Fetch only 1 similar book per recommendation

    for book_name in recommended_book_names:
        search_result = search_books(book_name, max_results)
        if search_result:
            simbooks.append(search_result[0])  

    # flash("Similar Books: {}".format(simbooks), "info")

   
    return render_template("similar.html", book=book, simbooks=simbooks)



# THIS WORKS ABOVE !!!!!!!!

if __name__ == "__main__":
    app.run(debug=True)
