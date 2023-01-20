#import game_war
import os
import datetime
import time
import pathlib
import pickle
import random
#import re

def ch(l):
    r = []
    for xx in l:
        x = xx.split(":")[1]
        if "you" in x:
            r.append(x.replace(" you   ", "").replace(" comp  ", "")[0] + x.replace(" you   ", "").replace(" comp  ", "")[1])
    return r


class Commit:

    def __init__(self, comment, game, l_c):
        self.player = game[0]
        self.ai = game[1]
        self.logs = game[2]
        self.comment = comment
        self.date = datetime.datetime.now()
        self.l_c = l_c

    def show_comment(self):
        return self.comment

    def show_date(self):
        return self.date

    def get_game(self):
        return [self.player, self.ai, self.logs]


class Branch:

    def __init__(self, name, c=-100):
        self.name = name
        self.commits = []
        self.curr_commit = c
        f = open(str(pathlib.Path().resolve())+"/git/"+self.name+".pickle", 'ab+')
        f.close()
        if os.path.getsize(str(pathlib.Path().resolve())+"/git/"+self.name+".pickle") > 0:
            fl = open(str(pathlib.Path().resolve())+"/git/"+self.name+".pickle", 'rb')
            self.commits = pickle.load(fl)
            fl.close()
        print("New branch {} created.".format(name))

    def load_next(self):
        if self.curr_commit == -100:
            print()
            print("No commit loaded!")
            return "NONE"
        else:
            if self.curr_commit+1 == len(self.commits): # было + 1
                print("No more commits.")
                return "NONE"
            else:
                self.curr_commit += 1
                #print(self.curr_commit)
                if self.curr_commit == len(self.commits) - 1:
                    print()
                    print("Last commit on Branch reached!")
                return self.load_commit(op=self.curr_commit)

    def load_past(self):
        if self.curr_commit == -100:
            print()
            print("No commit loaded!")
            return "NONE"
        else:
            if self.curr_commit-1 < 0:
                print("No more commits.")
                return "NONE"
            else:
                self.curr_commit -= 1
                #print(self.curr_commit)
                if self.curr_commit == 0:
                    print()
                    print("First commit on Branch reached!")
                return self.load_commit(op=self.curr_commit)

    def add_commit(self, game, op=-1, git=-1):
        if op == -1:
            commit = input("Commit: ")
        else:
            commit = "Commit " + str(random.randint(1, 1000))

        if len(self.commits) == 0:
            self.commits.append(Commit(comment=commit, game=game, l_c="first"))
            self.curr_commit = 0
        elif self.curr_commit + 1 == len(self.commits):
            xx = self.commits[-1]
            ll = []
            ll = self.commits[0].get_game()
            for x in range(1, len(self.commits)):
                ll[0] = self.commits[x].player
                ll[1] = self.commits[x].ai
                ll[2] = ll[2] + self.commits[x].logs
            xxx = []
            xxx.append(game[0])
            xxx.append(game[1])
            xxx.append(game[2][len(ll[2]):]) #["log"]
            self.commits.append(Commit(comment=commit, game=xxx, l_c=xx))
            self.curr_commit += 1
        else:
            if self.curr_commit == -100:
                name = self.name + "_" + str(random.randint(1000, 9999))
                #new = Branch(name[:18])
                git.branches.append(Branch(name[:20]))
                #git.branches.append(Branch(name))
                #git.branches[-1].commits = self.commits[:self.curr_commit+1]
                git.branches[-1].commits.append(Commit(comment=commit, game=game, l_c="first"))
                print("Done!")
                git.curr_branch = git.branches[-1]
                git.curr_branch.curr_commit = 0
                f = open(str(pathlib.Path().resolve())+"/git/"+name+".pickle", 'wb')
                pickle.dump(git.curr_branch.commits, f)
                f.close()
                fl = open(str(pathlib.Path().resolve())+"/git/"+name+".pickle", 'rb')
                git.curr_branch.commits = pickle.load(fl)
                fl.close()
            else:
                ll = []
                ll = self.commits[0].get_game()
                for x in range(1, self.curr_commit+1):
                    ll[0] = self.commits[x].player
                    ll[1] = self.commits[x].ai
                    ll[2] = ll[2] + self.commits[x].logs
                xxx = []
                xxx.append(game[0])
                xxx.append(game[1])
                xxx.append(game[2][len(ll[2]):])
                if xxx[1] != self.commits[self.curr_commit+1].ai and xxx[0] != self.commits[self.curr_commit+1].player:
                    name = self.name + "_" +  str(random.randint(1000, 9999))
                    #new = Branch(name[:18])
                    git.branches.append(Branch(name[:20]))
                    #git.branches.append(Branch(name))
                    git.branches[-1].commits = self.commits[:self.curr_commit+1]
                    git.branches[-1].commits.append(Commit(comment=commit, game=xxx, l_c=git.branches[-1].commits[-1]))
                    print("Done!")
                    git.curr_branch = git.branches[-1]
                    git.curr_branch.curr_commit = self.curr_commit + 1
                    #git.branches.append(new)



        self.curr_commit = len(self.commits) - 1
        f = open(str(pathlib.Path().resolve())+"/git/"+self.name+".pickle", 'wb')
        pickle.dump(self.commits, f)
        f.close()
        fl = open(str(pathlib.Path().resolve())+"/git/"+self.name+".pickle", 'rb')
        self.commits = pickle.load(fl)
        fl.close()
        print("Commit added.")

    def show_branch(self):
        os.system("cls")
        print("-" * 15)
        print(self.name)
        for i in range(0, len(self.commits)):
            e = self.commits[i].l_c
            print("{0} \t| {1} \t| {2} \t| {3} \t| {4}".format(i+1, self.commits[i].show_comment(), self.commits[i].show_date(), ch(self.commits[i].logs), e if e == "first" else e.comment))
        print("-" * 15)

    def remove_commit(self):
        self.show_branch()
        idx = int(input("Choose commit to remove: "))
        #self.commits.pop(idx-1)
        self.commits = self.commits[:idx-1]
        f = open(str(pathlib.Path().resolve())+"/git/"+self.name+".pickle", 'wb')
        pickle.dump(self.commits, f)
        f.close()
        fl = open(str(pathlib.Path().resolve())+"/git/"+self.name+".pickle", 'rb')
        self.commits = pickle.load(fl)
        fl.close()
        print("Commit removed.")

    def get_name(self):
        return self.name

    def load_commit(self, op=-1):
        if op == -1:
            self.show_branch()
            idx = int(input("Choose commit to load: "))
        else:
            idx = op + 1 # по счету
        self.curr_commit = idx - 1
        #return self.commits[idx-1].get_game()
        ll = []
        ll = self.commits[0].get_game()
        for x in range(1, idx):
            ll[0] = self.commits[x].player
            ll[1] = self.commits[x].ai
            ll[2] = ll[2] + self.commits[x].logs
        #self.commits = self.commits[:idx]
        f = open(str(pathlib.Path().resolve())+"/git/"+self.name+".pickle", 'wb')
        pickle.dump(self.commits, f)
        f.close()
        fl = open(str(pathlib.Path().resolve())+"/git/"+self.name+".pickle", 'rb')
        self.commits = pickle.load(fl)
        fl.close()
        return ll


class Git:

    def __init__(self):
        self.branches = []
        self.branches.append(Branch("master"))
        for file in os.listdir(str(pathlib.Path().resolve())+"/git/"):
            if file != "master.pickle":
                self.branches.append(Branch(file.replace(".pickle", "")))
        self.curr_branch = self.branches[0]

    def create_branch(self):
        name = input("New branch: ")
        self.branches.append(Branch(name))

    def show_branches(self):
        os.system("cls")
        print("-" * 15)
        for i in range(0, len(self.branches)):
            if self.branches[i] == self.curr_branch:
                print("{0}. {1} (current)".format(i+1, self.branches[i].get_name()))
            else:
                print("{0}. {1}".format(i+1, self.branches[i].get_name()))
        print("-" * 15)

    def remove_branch(self):
        self.show_branches()
        idx = int(input("Choose branch to remove: "))
        r_name = self.branches[idx-1].get_name()
        if self.branches[idx-1] == self.curr_branch:
            print("You can't remove current branch! Change the branch and then remove.")
        else:
            os.remove(str(pathlib.Path().resolve())+"/git/"+self.branches[idx-1].name + ".pickle")
            self.branches.pop(idx-1)
            print("Branch {0} removed.".format(r_name))

    def move_branch(self):
        self.show_branches()
        i = int(input("Choose the branch: "))
        self.curr_branch = self.branches[i-1]
        self.curr_branch.curr_commit = 0

    def get_curr(self):
        return self.curr_branch

    def git_menu(self):
        print("\t\t\t\t" + "-" * 15)
        print("\t\t\t\t|1. Show all branches.")
        print("\t\t\t\t|2. Show all commits on current branch.")
        print("\t\t\t\t|3. Change current branch.")
        print("\t\t\t\t|4. Create new branch.")
        print("\t\t\t\t|5. Remove branch.")
        print("\t\t\t\t|6. Add new commit.")
        print("\t\t\t\t|7. Remove commit.")
        print("\t\t\t\t|8. Load commit.")
        print("\t\t\t\t|9. Continue playing.")
        print("\t\t\t\t|0. Exit.")
        print("\t\t\t\t" + "-" * 15)

    def git_command(self, i):
        return {1: self.show_branches,
                2: self.curr_branch.show_branch,
                3: self.move_branch,
                4: self.create_branch,
                5: self.remove_branch,
                6: self.curr_branch.add_commit,
                7: self.curr_branch.remove_commit,
                8: self.curr_branch.load_commit,
                10: self.curr_branch.load_next,
                11: self.curr_branch.load_past,
                #9: exit,
                0: exit}.get(i, "Error!")

    def cycle(self):
        while True:
            #os.system("cls")
            self.git_menu()
            i = int(input("Choose command: "))
            if i == 6:
                game = "game"
                players = "pl"
                self.git_command(i)(game, players)
            else:
                self.git_command(i)()
