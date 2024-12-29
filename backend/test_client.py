import requests
import json

# Define the Flask app URL
BASE_URL = "http://127.0.0.1:5000"  # Adjust if your app runs on a different port


def test_query(query):
    """Sends a query to the Flask app and prints the response."""
    url = f"{BASE_URL}/query"
    data = {"query": query}

    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print("Response Data:")
        print(json.dumps(response.json(), indent=4))
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    test_query("bitcoin")  # Replace with your test query
