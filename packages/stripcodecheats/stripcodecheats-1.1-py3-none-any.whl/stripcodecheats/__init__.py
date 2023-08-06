from stripcodecheats.selenium_cheat import init
from stripcodecheats import github_requests
from stripcodecheats import cache

def start(github_username : str, github_password : str, github_token: str=None, executable_path: str = "chromedriver", iteration_count=True):
    github_requests.create_github(github_username, github_password, github_token)

    try:
        init(github_username, github_password, executable_path, iteration_count)
    
    except Exception as e:
        print(e)
        print("Exiting on Exception...")
    
    finally:
        print("Dumping Cache...")
        cache.dump_cache()