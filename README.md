# Github changelog

This tool creates a changelog for milestones in a Github repository. A great tool to create your release notes.

## Features

- Get a formatted list of all issues in a milestone
- Group issues by multiple labels
- Format as simple list or as tables

## Installation

```bash
$ git clone git@github.com:MartijnBraam/github-changelog.git
$ cd github-changelog
$ pip3 install -r requirements.txt
```

## Usage

```bash
# Create simple changelog list for v0.1 milestone
$ github-changelog MartijnBraam/github-changelog v0.1

# Create a changelog in table format
$ github-changelog --format table MartijnBraam/github-changelog v0.1

# Create a changelog grouped by labels
$ github-changelog --group-by bug --group-by feature --group-by security MartijnBraam/github-changelog v0.1
```

## Example output

This are some issues from the bootstrap project as example

### simple formatter output

## js

Fix behaviour of dropup when a click happened #16931
Carousel cleanups #16919
Button cleanups #16918
... more issues here ...

## feature

Added NuGet support #16710

## css

Use z-index 3 to show focus state on all sides of input #17007
Using grid inside modal misalignment #16902
.form-group-lg, .form-group-sm <label> has wrong line-height #16824
... more issues here ...

## Other

Have Travis CI use Ruby 2.0.0 #17012
Add Wall of Browser Bugs entry for #16988 #16994
Can't scroll <input type=text> on iPhone #16988
... more issues here ...

### table formatter output

## Other

| # | Title | Labels |
| - | ----- | ------ |
| #17012 | Have Travis CI use Ruby 2.0.0 | grunt |
| #16994 | Add Wall of Browser Bugs entry for #16988 | browser bug, docs |
| #16988 | Can't scroll <input type=text> on iPhone | browser bug, confirmed |

## feature

| # | Title | Labels |
| - | ----- | ------ |
| #16710 | Added NuGet support | feature, meta |

## css

| # | Title | Labels |
| - | ----- | ------ |
| #17007 | Use z-index 3 to show focus state on all sides of input | css |
| #16902 | Using grid inside modal misalignment | css, docs |
| #16824 | .form-group-lg, .form-group-sm <label> has wrong line-height | css |

## js

| # | Title | Labels |
| - | ----- | ------ |
| #16931 | Fix behaviour of dropup when a click happened | js |
| #16919 | Carousel cleanups | js |
| #16918 | Button cleanups | js |
