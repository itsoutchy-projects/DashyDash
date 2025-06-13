import requests

def GetAssets(name : str, repo : str)-> list[dict]:
    """
    Gets the latest release of the repository `repo` by `name` and returns its assets  
    You can use this as an array  
    Eg: `github.GetAssets('itsoutchy-projects', 'FNF-Launcher')[0]` - That returns the first uploaded asset in the latest release
    """
    resp = requests.get(f"https://api.github.com/repos/{name}/{repo}/releases/latest")
    return resp.json()["assets"]

def GetRelease(name : str, repo : str)-> dict:
    """
    Gets the latest release of the repository `repo` by `name` and returns it  
    You can use this as an dictionary  
    Eg: `github.GetReleases('itsoutchy-projects', 'FNF-Launcher')["url"]` - That returns the url of the latest release
    """
    resp = requests.get(f"https://api.github.com/repos/{name}/{repo}/releases/latest")
    return resp.json()