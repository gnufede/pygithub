#!/usr/bin/env python
# coding=utf8
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from os import walk, listdir
from os.path import join, isdir
import git 

app = Flask(__name__)
Bootstrap(app)
projectsDir = "./projects"
@app.route("/")
def directoryList():
    directoryList =  [ d for d in listdir(projectsDir)\
                      if isdir(join(projectsDir,d)) ]
    return render_template('dirlist.html',directoryList=directoryList)

@app.route("/<dirname>/<branch>")
@app.route("/<dirname>")
def repoDir(dirname=None, branch='master'):
    repo = git.Repo(join(projectsDir, dirname), odbt=git.GitDB)
    heads = repo.heads
    commits = repo.iter_commits(branch, max_count=100)
    return render_template('repoinfo.html',dirname=dirname, heads=heads,\
                           commits=commits, branch=branch)

@app.route("/<dirname>/commit/<commitsha>")
def commit(dirname=None, commitsha=None):
    repo = git.Repo(join(projectsDir, dirname), odbt=git.GitDB)
    if commitsha:
        commit = git.objects.base.Object.new(repo,commitsha)
        return render_template('commit.html', commit=commit)

if __name__ == "__main__":
    app.run(debug=True)
