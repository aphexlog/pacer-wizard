import requests
import dotenv
import os
import json

dotenv.load_dotenv()

API_KEY = os.getenv("API_KEY")

headers = {
    "Authorization": f"Token {API_KEY}"
}

BASE_URL = "https://www.courtlistener.com/api/rest/v4"

def fetch_clusters():
    response = requests.request("GET", BASE_URL + "/clusters", headers=headers)
    response = json.dumps(response.json(), indent=2)
    print(response)

def search(docket_number: str):
    # Use the docket_number as a query parameter in the search request
    params = {
        "docket_number": docket_number
    }
    response = requests.request("GET", BASE_URL + "/search/", headers=headers, params=params)
    response_data = response.json()

    # Optionally, return the response data to work with it further
    return response_data

def download_documents(search_results, save_dir='legal_documents'):
    # Create a directory for the downloaded documents
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for case in search_results['results']:
        case_name = case['caseName']
        docket_number = case['docketNumber']

        # Download each related opinion/document
        for opinion in case['opinions']:
            download_url = opinion.get('download_url')
            if download_url:
                case_dir = os.path.join(save_dir, f"{docket_number}_{case_name}")
                if not os.path.exists(case_dir):
                    os.makedirs(case_dir)

                local_filename = os.path.join(case_dir, os.path.basename(download_url))

                # Download the file
                response = requests.get(download_url)
                if response.status_code == 200:
                    with open(local_filename, 'wb') as file:
                        file.write(response.content)
                    print(f"Downloaded: {local_filename}")
                else:
                    print(f"Failed to download: {download_url}")
            else:
                print(f"No download URL for opinion in case {docket_number}")

def main():
    docket_number = "51281"  # Example docket number
    search_results = search(docket_number)
    # print(json.dumps(search_results, indent=2))

    # Download documents from the search results
    download_documents(search_results)

if __name__ == "__main__":
    main()
