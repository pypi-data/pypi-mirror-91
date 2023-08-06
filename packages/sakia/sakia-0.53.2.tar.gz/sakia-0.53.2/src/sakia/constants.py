import os

MAX_CONFIRMATIONS = 6

with open(
    os.path.join(os.path.dirname(__file__), "g1_license.html"), "r", encoding="utf-8"
) as stream:
    G1_LICENSE = stream.read()

GITLAB_RELEASES_PAGE_URL = "https://git.duniter.org/clients/python/sakia/-/releases"
GITLAB_RELEASES_API_URL = (
    "https://git.duniter.org/api/v4/projects/clients%2Fpython%2Fsakia/releases"
)
GITLAB_NEW_ISSUE_PAGE_URL = "https://git.duniter.org/clients/python/sakia/-/issues/new"
