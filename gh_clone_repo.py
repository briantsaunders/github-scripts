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
    gh_repo_to_clone: str = typer.Argument(
        "GH_REPO_TO_CLONE", envvar="GH_REPO_TO_CLONE"
    ),
    new_repo_name: str = typer.Argument("NEW_REPO_NAME", envvar="NEW_REPO_NAME"),
    webhook_url: str = typer.Argument("WEBHOOK_URL", envvar="WEBHOOK_URL"),
):
    """
    This is a simple python script that will create a repo from
    a template repo within an organization, add a team to it, and
    add a webhook.
    """
    git = Github(gh_token)
    service_account = git.get_user()
    try:
        git_org = git.get_organization(gh_org)
    except BadCredentialsException:
        logger.error("invalid github token, please check your token")
        sys.exit(1)
    except UnknownObjectException:
        logger.error(f"organization {gh_org} not found")
        sys.exit(1)
    try:
        template_repo = git_org.get_repo(gh_repo_to_clone)
    except UnknownObjectException:
        logger.error(f"repo {gh_repo_to_clone} not found in the org {gh_org}")
        sys.exit(1)
    try:
        repo = git_org.get_repo(new_repo_name)
        logger.info(f"repo {new_repo_name} already exists in the org {gh_org}")
    except UnknownObjectException:
        git_org.create_repo_from_template(new_repo_name, template_repo, private=True)
        repo = git_org.get_repo(new_repo_name)
        logger.info(f"repo {new_repo_name} created from template {gh_repo_to_clone}")
    try:
        git_team = git_org.get_team_by_slug(gh_team)
    except UnknownObjectException:
        logger.error(f"team {gh_team} not found in the org {gh_org}")
        sys.exit(1)
    git_team.add_to_repos(repo)
    git_team.update_team_repository(repo, "admin")
    repo.add_to_collaborators(service_account.login, permission="admin")
    webhooks = repo.get_hooks()
    for webhook in webhooks:
        if webhook.config["url"] == webhook_url:
            webhook.test()
            logger.info(
                f"webhook {webhook_url} already exists in the repo {new_repo_name}"
            )
            sys.exit(1)
    webhook = repo.create_hook(
        "web", {"url": webhook_url, "content_type": "json"}, ["push"], active=True
    )
    webhook.test()


if __name__ == "__main__":
    typer.run(main)
