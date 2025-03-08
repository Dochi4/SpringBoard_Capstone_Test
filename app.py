@app.route('/bookrecommendation/<volume_id>', methods=["GET", "POST"])
def bookrecommendation(volume_id):
    """Fetch AI book recommendations and find similar books."""
    book = get_volume_id(volume_id)
    if not book:
        return redirect(f"/bookpreview/{volume_id}")

    # Get AI recommendations by calling /bookaifetch/<volume_id>
    ai_response = similar_book_ai(book)



    recommendations = ai_response.get("Recommendations", [])  

    simbooks = []
    max_results = 1  # Fetch only 1 similar book per recommendation

    for recommendation in recommendations:
        book_title = recommendation["title"]
        reason = recommendation["reason"]  # Get the correct reason for this book

        search_result = search_books(book_title, max_results)
        if search_result:
            simbook_entry = search_result[0]  # Get the first matching book
            simbook_entry["reason"] = reason  # Attach the correct reason
            simbooks.append(simbook_entry)  # Append the modified book

    return render_template("similar.html", book=book, simbooks=simbooks)
