#!/usr/bin/env python
# coding=utf8
from flask import Flask, render_template, redirect, url_for,\
                send_from_directory
from flask.ext.bootstrap import Bootstrap
from os import walk, listdir, makedirs, getlogin
from os.path import join, isdir, abspath
import git

app = Flask(__name__)
Bootstrap(app)
projectsDir = "./projects"
hostname = [app.config['SERVER_NAME'], 'localhost']\
                [int(app.config['SERVER_NAME'] is None)]

if not isdir(projectsDir):
    makedirs(projectsDir)

def getRepoUrl(dirname):
    return ''.join((getlogin(), '@', hostname, ':', abspath(dirname)))

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
                            repoUrl = getRepoUrl(join(projectsDir,dirname)),
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
