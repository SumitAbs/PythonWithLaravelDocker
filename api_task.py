import requests

def fetch_data():
    # URL of a public placeholder API
    url = "https://jsonplaceholder.typicode.com/posts/10"

    try:
        # Making a GET request to the API
        response = requests.get(url)

        # Checking if the request was successful (Status Code 200)
        if response.status_code == 200:
            # Parsing the JSON response into a Python Dictionary (similar to Associative Array in PHP)
            data = response.json()
            
            print("Successfully fetched data:")
            print(f"Title: {data['title']}")
            print(f"Body: {data['body']}")
        else:
            print(f"Failed to fetch data. Status Code: {response.status_code}")

    except Exception as e:
        # Handling any potential network or request errors
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_data()