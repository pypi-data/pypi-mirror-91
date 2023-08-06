from reposherlock.client import APIClient


class GitHub:
    """Provides a simplistic interface to retrieve information from the GitHub API.
    """

    GITHUB_DIFF = 'application/vnd.github.diff'
    GITHUB_PATCH = 'application/vnd.github.patch'
    GITHUB_JSON = 'application/vnd.github+json'
    API_PREFIX = 'https://api.github.com/'

    def __init__(self, username, token):
        """Constructor method

        :param username: The username that identifies the query's author
        :type username: str
        :param token: The hex-string that GitHub generates as a means of authenticating 3rd party applications
        :type token: str
        """
        self.credentials = {
            'user': username,
            'token': token
        }
        self.headers = {
            # We're starting out simple, only basic JSON retrieval for now.
            'Accept': self.GITHUB_JSON
        }
        self.client = APIClient(self.credentials, False, self.headers)

    def get_issues(self, repo_slug, pages=1000):
        """Fetches all issues attached to a particular repository.

        :param repo_slug: A string representing the repository endpoint as <owner>/<repository>
        :type repo_slug: str
        :param pages: The maximum number of pages the client should pull, default is 1000
        :type pages: int
        :return: A python list containing all issues attached to the provided repository
        :rtype: list
        """
        issue_page = 1
        issues = list()
        issues_endpoint = "repos/%s/issues" % repo_slug
        issues_endpoint_uri = self.API_PREFIX + issues_endpoint
        # Fetch the actual issues
        while issue_page <= pages:
            result = self.client.query_endpoint(issues_endpoint_uri, parameters={'page': issue_page, 'state': 'all'})
            if isinstance(result, list) and len(result) > 0:
                issues.extend(result)
            else:
                # The result is a message or something we did not expect.
                break
            issue_page += 1
        # Go over all the issues again and fetch the comments
        for issue in issues:
            if issue['comments'] > 0:
                comments = []
                comments_endpoint = "repos/%s/issues/%d/comments" % (repo_slug, issue['number'])
                comments_endpoint_uri = self.API_PREFIX + comments_endpoint
                comments_page = 1
                while comments_page <= pages:
                    result = self.client.query_endpoint(comments_endpoint_uri, parameters={'page': comments_page})
                    if isinstance(result, list) and len(result) > 0:
                        comments.extend(result)
                    else:
                        # The result is a message or something we did not expect.
                        break
                    comments_page += 1
                issue['issue_comments'] = comments
        return issues

    def get_pull_requests(self, repo_slug, pages=1000):
        """Fetches all pull requests attached to a particular repository.

        :param repo_slug: A string representing the repository endpoint as <owner>/<repository>
        :type repo_slug: str
        :param pages: The maximum number of pages the client should pull, default is 1000
        :type pages: int
        :return: A python list containing all pull requests attached to the provided repository
        :rtype: list
        """
        pull_request_page = 1
        pull_requests = list()
        pull_requests_endpoint = "repos/%s/pulls" % repo_slug
        pull_requests_endpoint_uri = self.API_PREFIX + pull_requests_endpoint
        # Fetch the actual pull_requests
        while pull_request_page <= pages:
            result = self.client.query_endpoint(
                pull_requests_endpoint_uri, parameters={'page': pull_request_page, 'state': 'all'}
            )
            if isinstance(result, list) and len(result) > 0:
                pull_requests.extend(result)
            else:
                # The result is a message or something we did not expect.
                break
            pull_request_page += 1
        # Go over all the pull_requests again and fetch the comments
        for pull_request in pull_requests:
            comments = []
            # Because, in its heart of hearts, GitHub treats pull requests as issues
            comments_endpoint = "repos/%s/issues/%d/comments" % (repo_slug, pull_request['number'])
            comments_endpoint_uri = self.API_PREFIX + comments_endpoint
            comments_page = 1
            while comments_page <= pages:
                result = self.client.query_endpoint(comments_endpoint_uri, parameters={'page': comments_page})
                if isinstance(result, list) and len(result) > 0:
                    comments.extend(result)
                else:
                    # The result is a message or something we did not expect.
                    break
                comments_page += 1
            pull_request['pull_request_comments'] = comments
        # Go over all the pull_requests again and fetch the review comments
        for pull_request in pull_requests:
            reviews = []
            reviews_endpoint = "repos/%s/pulls/%d/comments" % (repo_slug, pull_request['number'])
            reviews_endpoint_uri = self.API_PREFIX + reviews_endpoint
            reviews_page = 1
            while reviews_page <= pages:
                result = self.client.query_endpoint(reviews_endpoint_uri, parameters={'page': reviews_page})
                if isinstance(result, list) and len(result) > 0:
                    reviews.extend(result)
                else:
                    # The result is a message or something we did not expect.
                    break
                reviews_page += 1
            pull_request['pull_request_reviews'] = reviews
        # Go over all the pull_requests again and fetch the statuses
        for pull_request in pull_requests:
            statuses = []
            status_number = pull_request['head']['sha']
            statuses_endpoint = "repos/%s/statuses/%s" % (repo_slug, status_number)
            statuses_endpoint_uri = self.API_PREFIX + statuses_endpoint
            statuses_page = 1
            while statuses_page <= pages:
                result = self.client.query_endpoint(statuses_endpoint_uri, parameters={'page': statuses_page})
                if isinstance(result, list) and len(result) > 0:
                    statuses.extend(result)
                else:
                    # The result is a message or something we did not expect.
                    break
                statuses_page += 1
            pull_request['pull_request_statuses'] = statuses
        # Go over all the pull_requests again and fetch their relevant commits
        for pull_request in pull_requests:
            commits = []
            commits_endpoint = "repos/%s/pulls/%d/commits" % (repo_slug, pull_request['number'])
            commits_endpoint_uri = self.API_PREFIX + commits_endpoint
            commits_page = 1
            while commits_page <= pages:
                result = self.client.query_endpoint(commits_endpoint_uri, parameters={'page': commits_page})
                if isinstance(result, list) and len(result) > 0:
                    commits.extend(result)
                else:
                    # The result is a message or something we did not expect.
                    break
                commits_page += 1
            pull_request['pull_request_commits'] = commits
        return pull_requests

    def get_commits(self, repo_slug, pages=1000):
        """Fetches all commits, commit comments, and commit reviews attached to a particular repository.

        :param repo_slug:
        :param pages:
        :return:
        """
        commit_page = 1
        commits = list()
        commits_endpoint = "repos/%s/commits" % repo_slug
        commits_endpoint_uri = self.API_PREFIX + commits_endpoint
        # Fetch the actual commits
        while commit_page <= pages:
            result = self.client.query_endpoint(commits_endpoint_uri, parameters={'page': commit_page, 'state': 'all'})
            if isinstance(result, list) and len(result) > 0:
                commits.extend(result)
            else:
                # The result is a message or something we did not expect.
                break
            commit_page += 1
        # Go over all the commits again and fetch the comments
        for commit in commits:
            comments = []
            comments_endpoint = "repos/%s/commits/%s/comments" % (repo_slug, commit['sha'])
            comments_endpoint_uri = self.API_PREFIX + comments_endpoint
            comments_page = 1
            while comments_page <= pages:
                result = self.client.query_endpoint(comments_endpoint_uri, parameters={'page': comments_page})
                if isinstance(result, list) and len(result) > 0:
                    comments.extend(result)
                else:
                    # The result is a message or something we did not expect.
                    break
                comments_page += 1
            commit['commit_comments'] = comments
        return commits
