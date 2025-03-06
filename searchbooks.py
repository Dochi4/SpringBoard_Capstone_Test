import os
import requests


GOOGLE_BOOKS_API_KEY = os.environ.get("GOOGLE_BOOKS_API_KEY")
GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"


DEFAULT_IMAGE = "https://as1.ftcdn.net/v2/jpg/03/77/19/40/1000_F_377194073_LHGUkaGPCzOdRcuBQ40XBtrnpfJLa6hm.jpg"

def search_books(query, max_results):
    """Search Google Books API using a query and return book details."""
    params = {
        'q': query,
        'maxResults': max_results,
        'key': GOOGLE_BOOKS_API_KEY
    }

    try:
        response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
        response.raise_for_status()  
        data = response.json()
    except requests.RequestException as e:
        print(f"API Error: {str(e)}")
        return []

    books = []
    for item in data.get("items", []):
        volume_info = item.get("volumeInfo", {})
        access_info = item.get("accessInfo", {})

        books.append({
            "volume_id": item.get("id"),  
            "title": volume_info.get("title", "Untitled"),
            "authors": volume_info.get("authors", ["Unknown Author"]),
            "thumbnail": volume_info.get("imageLinks", {}).get("thumbnail", DEFAULT_IMAGE),
            "categories": volume_info.get("categories", ["Uncategorized"]),
            "preview_link": volume_info.get("previewLink", ""),
            "viewability": access_info.get("viewability", "UNKNOWN"),
            "published_date": volume_info.get("publishedDate", "Unknown")
        })

    return books

def get_volume_id(volume_id):
    """Fetch a book directly from Google Books API using its Volume ID."""
    url = f"{GOOGLE_BOOKS_API_URL}/{volume_id}?key={GOOGLE_BOOKS_API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"Error fetching book: {e}")
        return None

    volume_info = data.get("volumeInfo", {})
    access_info = data.get("accessInfo", {})
    
    return {
        "volume_id": data.get("id"),
        "title": volume_info.get("title", "Untitled"),
        "authors": volume_info.get("authors", ["Unknown Author"]),
        "thumbnail": volume_info.get("imageLinks", {}).get("thumbnail", DEFAULT_IMAGE),
        "description": volume_info.get("description", "No description available"),
        "categories": volume_info.get("categories", ["Uncategorized"]),
        "preview_link": volume_info.get("previewLink", ""),
        "viewability": access_info.get("viewability", "UNKNOWN"),
        "published_date": volume_info.get("publishedDate", "Unknown")
    }


