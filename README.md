# Github changelog

This tool creates a changelog for milestones in a Github repository. A great tool to create your release notes.

## Features

- Get a formatted list of all issues in a milestone
- Group issues by multiple labels
- Format as simple list or as tables

## Usage

```bash
# Create simple changelog list for v0.1 milestone
$ github-changelog MartijnBraam/github-changelog v0.1

# Create a changelog in table format
$ github-changelog --format table MartijnBraam/github-changelog v0.1

# Create a changelog grouped by labels
$ github-changelog --group-by bug --group-by feature --group-by security MartijnBraam/github-changelog v0.1
```