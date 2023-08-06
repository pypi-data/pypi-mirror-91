import os
from git import Git
from urllib.parse import urlparse

VPACKAGE_JSON = 'vpackage.json'
VPACKAGE_HIDDEN = '.vpackage'
REPOS = 'repos'

def is_vivp_dir(d):
    return os.path.exists(os.path.join(d, VPACKAGE_JSON))
    if not os.path.exists(os.path.join(d, VPACKAGE_JSON)):
        return False
    # TODO : Validate the vpackage.json file

    try: # Check if git repo
        g = Git(d)
        g.remote()
    except:
        return False

    return True

def is_vivp_file(d):
    try:
      open(d, "r")
      return True
    except IOError:
      return False
    

def is_valid_git_url(u):
    try:
        a = urlparse(u)
        if a.netloc == "github.com":
            return True
        else:
            return False
    except:
        return False
    return True

def get_cache_dir(vivp_dir):
    return os.path.join(vivp_dir, VPACKAGE_HIDDEN)

def get_repos_dir(vivp_dir):
    return os.path.join(vivp_dir, VPACKAGE_HIDDEN, REPOS)