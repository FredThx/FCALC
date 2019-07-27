'''
Github class for use Github API V3 to check if a new release is available on Github
'''

import requests


class Github:
    '''Github API V3
    '''
    api_url = "https://api.github.com/repos/"

    def __init__(self, owner = None, repo = None):
        '''Initialisation
            - api_url       default = https://api.github.com/repos/
            - owner         default = None
            - repo         default = None
        '''
        self.owner = owner
        self.repo = repo

    def get_last_release(self, owner = None, repo = None):
        ''' Get the last release information : a dict
        '''
        owner = owner or self.owner
        assert owner, "Owner must be specified"
        repo = repo or self.repo
        assert repo, "Repo must be specified"
        try:
            r = requests.get(Github.api_url+owner+"/"+repo+"/releases/latest")
            return r.json()
        except:
            pass

    def url_update(self, actual_version,**kwargs):
        '''If a new release is available, return the download url
        '''
        last_release = self.get_last_release(**kwargs)
        if last_release and last_release['tag_name'] > actual_version:
            return last_release['assets'][0]['browser_download_url']
