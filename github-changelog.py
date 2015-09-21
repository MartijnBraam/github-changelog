#!/usr/bin/env python3
from github import Github
from configparser import ConfigParser
from argparse import ArgumentParser
from collections import OrderedDict
import os
import xdg.BaseDirectory
import re

# Resolve the XDG config path
config_dir = xdg.BaseDirectory.save_config_path('github-changelog')
config_file = os.path.join(config_dir, "config.ini")

# First time setup
if not os.path.isfile(config_file):
    print("No configuration found. Starting initial setup.")
    print("Github-changelog needs a token to communicate with github.")
    print("Please create a token on https://github.com/settings/tokens")
    token = input("Your personal access token: ")
    config = ConfigParser()
    config.add_section("general")
    config.set("general", "token", token)
    with open(config_file, "w") as config_handle:
        config.write(config_handle)

# Initialize Github connection
config = ConfigParser()
config.read(config_file)
token = config['general']['token']
github = Github(token)

# Check if we're already in a github repo
current_path = os.getcwd().split("/")
repo_path = None
for length in range(len(current_path), 0, -1):
    test_path = "/".join(current_path[0:length])
    possible_git_dir = os.path.join(test_path, ".git")
    if os.path.isdir(possible_git_dir):
        repo_path = possible_git_dir
        break

# Search for a github repository in the git config
github_repo_id = None
if repo_path:
    regex_repo_id = re.compile(r'[:/]([^/]*/[^/]*)\.git')
    git_config = ConfigParser()
    git_config.read(os.path.join(repo_path, "config"))
    for section in git_config.sections():
        if 'remote' in section:
            remote_url = git_config[section]['url']
            github_repo_id = regex_repo_id.search(remote_url)
            if github_repo_id:
                github_repo_id = github_repo_id.group(1)
                break

# Parse the command line arguments
argparse = ArgumentParser(description="Changelog generator for Github")
argparse.add_argument("-f", "--format", help="Output format", default="simple", action="store",
                      choices=["simple", "table"])
argparse.add_argument("-g", "--group-by", help="Group output by github labels, use multiple times for every label",
                      action="append")
if not github_repo_id:
    argparse.add_argument("repository", help="The github repository in user/repo format")
argparse.add_argument("milestone", help="The milestone to create a changelog for", action="store")

args = argparse.parse_args()

# Resolve the milestone argument to a milestone object on github
if github_repo_id:
    repository_name = github_repo_id
else:
    repository_name = args.repository
repository = github.get_repo(github_repo_id)
milestone = None
for m in repository.get_milestones():
    if m.title == args.milestone:
        milestone = m

if not milestone:
    print("Cannot find milestone {} in repository {}".format(args.milestone, github_repo_id))
    exit(1)

# Set up grouping
groups = {}
grouping = False
if args.group_by:
    grouping = True
    for group in args.group_by:
        groups[group] = []
    groups["Other"] = []
else:
    groups["Issues"] = []

# Retrieve and group all github issues for the milestone
issues = repository.get_issues(milestone=milestone, state="all")
for issue in issues:
    if not grouping:
        groups["Issues"].append(issue)
        continue

    labels_github = issue.labels
    labels = []
    for l in labels_github:
        labels.append(l.name)
    intersect = list(set(args.group_by) & set(labels))
    if len(intersect) == 0:
        intersect = ["Other"]
    for label in intersect:
        groups[label].append(issue)

# Remove empty groups

for group in list(groups.keys()):
    if len(groups[group]) == 0:
        groups.pop(group)

# if grouping is used then order the groups to the same order as that the arguments are passed to the script
# and always sort the "Other" group last if it exists

if grouping:
    ordered_groups = OrderedDict()
    for group in args.group_by:
        if group == "Other":
            continue
        if group in groups:
            ordered_groups[group] = groups[group]
    if "Other" in groups:
        ordered_groups["Other"] = groups["Other"]
    groups = ordered_groups

# Feed the grouped issues to a formatter
if args.format == "simple":
    """
    ## Group name

    - The issue title #1
    - Another issue #2
    """
    for group in groups:
        print("## {}\n".format(group))
        for issue in groups[group]:
            print("- {} #{}".format(issue.title, issue.number))
        print("")

if args.format == "table":
    """
    ## Group name

    | #   | Title | Labels |
    | --- | ----- | ------ |
    | 1   | The.. | bla bl |
    """
    for group in groups:
        print("## {}\n".format(group))
        print("| # | Title | Labels |")
        print("| --- | ----- | ------ |")
        for issue in groups[group]:
            labels = []
            for l in issue.labels:
                labels.append(l.name)
            labels = ", ".join(labels)
            print("| #{} | {} | {} |".format(issue.number, issue.title, labels))
        print("")
