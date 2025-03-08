import os
from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from dotenv import load_dotenv
from searchbooks import search_books, get_volume_id
from deepseekai import ask_ai, similar_book_ai , similar_descript_ai
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

@app.route('/bookrecommendation/<volume_id>', methods=["GET", "POST"])
def bookrecommendation(volume_id):
    """Fetch AI book recommendations and find similar books."""
    book = get_volume_id(volume_id)
    if not book:
        return redirect(f"/bookpreview/{volume_id}")

    # Get AI recommendations by calling the AI function
    ai_response = similar_book_ai(book)
    # Check for error in AI response
    if "error" in ai_response:
        flash(f"AI Error: {ai_response['error']}", "error")
        return redirect(f"/bookpreview/{volume_id}")

    recommendations = ai_response.get("Recommendations", [])
    simbooks = []
    max_results = 1  # Fetch only 1 similar book per recommendation

    for recommendation in recommendations:
        # Use .get() to avoid KeyError if keys are missing
        book_title = recommendation.get("title")
        reason = recommendation.get("reason")
        if not book_title:
            continue

        search_result = search_books(book_title, max_results)
        if search_result:
            simbook_entry = search_result[0]
            simbook_entry["reason"] = reason  # Attach the correct reason
            simbooks.append(simbook_entry)

    return render_template("similar.html", book=book, simbooks=simbooks)


@app.route('/bookrecommendation/description', methods=["GET", "POST"])
def descriptionrecommendation():
    """Fetch AI similar books based on user's description."""
    
    if request.method == "POST":
        user_description = request.form.get("user_description")

    

        if not user_description:  # Ensure user provides input
            flash("Please enter a book description!", "warning")
            return redirect(request.url)

        recommendations = []
        
        ai_response = similar_descript_ai(user_description)

        if not ai_response:
            print("AI Response is empty or invalid.") 

        recommendations = ai_response.get("Recommendations", [])  

        simbooks = []

        max_results = 1 

        for recommendation in recommendations:
            book_title = recommendation["title"]
            reason = recommendation["reason"]  

            search_result = search_books(book_title, max_results)
            if search_result:
                simbook_entry = search_result[0]  
                simbook_entry["reason"] = reason  
                simbooks.append(simbook_entry) 

        return render_template("similar.html", user_description=user_description, simbooks=simbooks)

    
    return redirect("/search")




if __name__ == "__main__":
    app.run(debug=True)
