#taken from this StackOverflow answer: https://stackoverflow.com/a/39225039
# https: // github.com/thoppe/streamlit-skyAR/blob/master/GD_download.py

# When downloading large files from Google Drive, a single GET request is not sufficient.
# A second one is needed, and this one has an extra URL parameter called confirm, 
# whose value should equal the value of a certain cookie.


import requests


def download_file(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
