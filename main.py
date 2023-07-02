import requests
import hashlib
import sys


def sha256_hash(string):
    """Calculates the SHA-256 hash of a string."""
    hash_object = hashlib.sha256()
    hash_object.update(string.encode("utf-8"))
    return hash_object.hexdigest()


def fetch_owner(access_key):
    repos = []
    page = 1
    per_page = 1
    headers = {"Authorization": f"token {access_key}"}
    url = f"https://api.github.com/user"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        me = response.json()
        print(f"Found user: {me['login']}")
        return me["login"]
    else:
        print(f"Error fetching user name: {response.status_code}")
        return ""


def download_pipeline_log(repo_name, pipeline_id, access_key):
    url = "https://api.github.com/repos/{}/{}/actions/runs/{}/logs".format(
        fetch_owner(access_key), repo_name, pipeline_id
    )
    response = requests.get(url, headers={"Authorization": f"token {access_key}"})
    if response.status_code == 200:
        print("Found pipeline, saving it to disk")
        log = response.content
        return log
    else:
        return None


if __name__ == "__main__":
    print(
        f"Pipeline fetcher called with repository name: {sys.argv[1]} pipeline id: {sys.argv[2]} and hashed token: {sha256_hash(sys.argv[3])}"
    )

    repo_name = sys.argv[1]
    pipeline_id = sys.argv[2]
    access_key = sys.argv[3]

    log = download_pipeline_log(repo_name, pipeline_id, access_key)
    with open("pipeline.zip", "wb") as f:
        f.write(log)
