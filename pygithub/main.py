#!/usr/bin/env python
# coding=utf8
from flask import Flask, render_template, redirect, url_for
from flask.ext.bootstrap import Bootstrap
from os import walk, listdir, makedirs
from os.path import join, isdir
import git

app = Flask(__name__)
Bootstrap(app)
projectsDir = "./projects"

if not isdir(projectsDir):
    makedirs(projectsDir)

@app.route("/")
def directoryList():
    directoryList =  [d for d in listdir(projectsDir)\
                      if isdir(join(projectsDir,d))]
    return render_template('dirlist.html',directoryList=directoryList)

@app.route("/new/<dirname>")
def createRepo(dirname=None):
    if dirname:
        repo = git.Repo.init(join(projectsDir, dirname), bare=True)
        return redirect("/"+dirname)

@app.route("/<dirname>/<branch>")
@app.route("/<dirname>")
def repoDir(dirname=None, branch='master'):
    repo = git.Repo(join(projectsDir, dirname), odbt=git.GitDB)
    heads = repo.heads
    commits = repo.iter_commits(branch, max_count=100)
    return render_template('repoinfo.html',
                            dirname=dirname,
                            heads=heads,
                            commits=commits,
                            branch=branch)

@app.route("/<dirname>/commit/<commitsha>")
def commit(dirname=None, commitsha=None):
    repo = git.Repo(join(projectsDir, dirname), odbt=git.GitDB)
    heads = repo.heads
    if commitsha:
        commit = git.objects.base.Object.new(repo,commitsha)
        diffindexes = [diff.diff.split('\n') for x in commit.parents
                        for diff in x.diff(commit, create_patch=True)]
        return render_template('commit.html',
                                commit=commit,
                                diffs=diffindexes,
                                dirname=dirname,
                                heads=heads)

if __name__ == "__main__":
    app.run(debug=True)
