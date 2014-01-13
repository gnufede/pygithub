#!/usr/bin/env python
# coding=utf8
from flask import Flask, render_template, send_from_directory
from flask.ext.bootstrap import Bootstrap
from os import listdir, makedirs, getlogin
from os.path import join, isdir, abspath
import git

hostname = '' # Define here the hostname to access the repo
user = 'peine' # Define here the user you would use to access the repo
projectsDir = './projects' # Define here the directory for projects

app = Flask(__name__)
Bootstrap(app)

hostname = hostname or app.config['SERVER_NAME'] or 'localhost'
user = user or getlogin()
repoUrl = ''.join((user, '@', hostname, ':', abspath(projectsDir)))

if not isdir(projectsDir):
    makedirs(projectsDir)

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(join(app.root_path, 'static'),
                           'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/")
def directoryList():
    directoryList =  [d for d in listdir(projectsDir)\
                      if git.repo.fun.is_git_dir(join(projectsDir,d))]
    return render_template('dirlist.html',directoryList=directoryList)

@app.route("/<dirname>/<branch>")
@app.route("/<dirname>")
def repoDir(dirname=None, branch='master'):
    if dirname and not git.repo.fun.is_git_dir(join(projectsDir,dirname)):
        repo = git.Repo.init(join(projectsDir, dirname), bare=True)
    else:
        repo = git.Repo(join(projectsDir, dirname), odbt=git.GitDB)
    return render_template('repoinfo.html',
                            repoUrl = '/'.join((repoUrl, dirname)),
                            dirname=dirname,
                            heads=repo.heads,
                            commits=repo.iter_commits(branch, max_count=100),
                            branch=branch)

@app.route("/<dirname>/commit/<commitsha>")
def commit(dirname=None, commitsha=None):
    repo = git.Repo(join(projectsDir, dirname), odbt=git.GitDB)
    if commitsha:
        commit = git.objects.base.Object.new(repo,commitsha)
        diffindexes = [diff.diff.split('\n') for x in commit.parents
                        for diff in x.diff(commit, create_patch=True)]
        return render_template('commit.html',
                                commit=commit,
                                diffs=diffindexes,
                                dirname=dirname,
                                heads=repo.heads)

if __name__ == "__main__":
    app.run(debug=True)
