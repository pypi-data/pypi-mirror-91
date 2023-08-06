from github import Github
import time
import random
from stripcodecheats.cache import repo_cache, Repo

EXTENSIONS = ["py", "js", "ts", "rb", "html", "swift", "c", "m", "sh", "java", "cpp", "go", "php"]

g = None

def create_github(github_username: str, github_password: str, github_token: str):
    global g

    if github_token == None:
        g = Github(login_or_token=github_username, password=github_password)
        return
    
    g = Github(login_or_token=github_token)

def search_repos_for_file_name(filename, repo_ids):
    for i, repo_id in enumerate(repo_ids):
        repo = repo_cache.get_repo_if_exists(repo_id)
        if repo:
            filename = filename.replace("redacted", repo.name)
            
            if repo.filename_exists(filename):
                return i
        
        else:
            repo = g.get_repo(repo_id)

            filename = filename.replace("redacted", repo.name)

            cache_repo = Repo(repo.name)
            branch = repo.get_branch(repo.default_branch)
            tree = repo.get_git_tree(branch.commit.sha, recursive=True).tree

            return_index = None
            for file in tree:
                check_filename = file.path.split("/")[-1]
                # if filename has a valid extension for the languages
                if check_filename.split(".")[-1] in EXTENSIONS:
                    cache_repo.add_filename(check_filename)
                
                    if filename == check_filename:
                        return_index = i
            
            # add repo to cache if no errors and tree has been parsed
            repo_cache.add_repo(repo_id, cache_repo)

            if return_index != None:
                return return_index
    
    # choose random if cannot find file
    return random.choice(range(len(repo_ids)))