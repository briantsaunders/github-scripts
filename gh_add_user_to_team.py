import sys

import typer
from dotenv import load_dotenv
from github import Github, UnknownObjectException, BadCredentialsException
from loguru import logger

load_dotenv()


def main(
    gh_token: str = typer.Argument("GH_TOKEN", envvar="GH_TOKEN"),
    gh_org: str = typer.Argument("GH_ORG", envvar="GH_ORG"),
    gh_team: str = typer.Argument("GH_TEAM", envvar="GH_TEAM"),
    username_to_add: str = typer.Argument(
        "USERNAME_TO_ADD", envvar="USERNAME_TO_ADD", help="username to add to the team"
    ),
):
    """
    This is a simple python script that will add a user to a github team
    within an organization.
    """
    git = Github(gh_token)
    try:
        user = git.get_user(username_to_add)
    except BadCredentialsException:
        logger.error("invalid github token, please check your token")
        sys.exit(1)
    except UnknownObjectException:
        logger.error(f"username {username_to_add} not found in github")
        sys.exit(1)
    try:
        git_org = git.get_organization(gh_org)
    except UnknownObjectException:
        logger.error(f"organization {gh_org} not found")
        sys.exit(1)
    if not git_org.has_in_members(user):
        logger.error(f"username {user.login} not found in the org {gh_org}")
        sys.exit(1)
    try:
        git_team = git_org.get_team_by_slug(gh_team)
    except UnknownObjectException:
        logger.error(f"team {gh_team} not found in the org {gh_org}")
        sys.exit(1)
    if git_team.has_in_members(user):
        logger.error(f"username {user.login} already in the team {gh_team}")
        sys.exit(1)
    git_team.add_membership(user, role="member")


if __name__ == "__main__":
    typer.run(main)
