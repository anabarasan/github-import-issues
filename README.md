github-import-issues
====================

Import milestones, labels &amp; Issues from one repository to another
This uses Github API v3.

Configuration
=============

Edit config.py and set 
* GITHUB_USERNAME
* GITHUB_PASSWORD
* SOURCE_REPO <owner>/<repository>
* TARGET_REPO <owner>/<repository>

Run
===

execute migrate.py
all milestones, labels &amp; issues will be moved from source repository to target repository
