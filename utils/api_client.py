import requests

def get_post_data(post_id):
    """
    Fetches post data from a placeholder API based on ID.
    """
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    try:
        response = requests.get(url)
        # Raise an exception for 4xx or 5xx status codes
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}