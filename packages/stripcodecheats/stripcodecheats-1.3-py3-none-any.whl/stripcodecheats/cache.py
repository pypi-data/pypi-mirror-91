import os
import pickle

class Repo():
    def __init__(self, name):
        self.name = name
        self.filenames = []
    
    def add_filename(self, filename):
        self.filenames.append(filename)
    
    def filename_exists(self, filename):
        return filename in self.filenames

class Cache():
    def __init__(self):
        self.repo_id_store = {}

    def dump(self):
        pickle.dump(self)
    
    def add_repo(self, repo_id, repo):
        self.repo_id_store[repo_id] = repo

    def repo_exists(self, repo_id):
        return self.repo_id_store.get(repo_id) != None

    def get_repo_if_exists(self, repo_id):
        repo = self.repo_id_store.get(repo_id)

        if repo == None:
            return False
        
        return repo

def load_cache():
    if os.path.isfile("cache/repo_cache.pkl"):
        with open("cache/repo_cache.pkl", "rb") as f:
            cache_init = pickle.load(f)

    else:
        cache_init = Cache()

    return cache_init

repo_cache = load_cache()

def dump_cache():
    if not os.path.isdir("cache"):
        os.mkdir("cache")

    with open("cache/repo_cache.pkl", "wb") as f:
        pickle.dump(repo_cache, f)