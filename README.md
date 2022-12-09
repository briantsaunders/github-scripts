# Github Demo Scripts

The repo contains simple python based scripts for interacting with the Github API.

### Add User to Org Team

Example of adding a user to a github team that exists within an organization.

Required environment vars (should be defined in a .env file):

- `GH_TOKEN`: Github token of account attempting to run the script.
- `GH_ORG`: Github organization where team exists.
- `GH_TEAM`: Github team to add user to.
- `USERNAME_TO_ADD`: Github username to add to team.

How to run:

```python
python gh_add_user_to_team.py
```

### Clone Template

Example of creating a new repo from an orgnization template, adds a team to newly 
created repo, sets team as admins, and adds a webhook.

Required environment vars (should be defined in a .env file):

- `GH_TOKEN`: Github token of account attempting to run the script.
- `GH_ORG`: Github organization where team exists.
- `GH_TEAM`: Github team to add user to.
- `GH_REPO_TO_CLONE`: Github template repo.
- `NEW_REPO_NAME`: New repo name.
- `WEBHOOK_URL`: Webhook url to add.

How to run:

```python
python gh_clone_repo.py
```