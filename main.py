from utils.api_client import get_post_data

def run_app():
    # Attempt to fetch data for post ID 1
    result = get_post_data(1)
    
    if "error" in result:
        print(f"Operation failed: {result['error']}")
    else:
        print(f"Success! Post Title: {result['title']}")

if __name__ == "__main__":
    run_app()

    