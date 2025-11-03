# Pushing a local folder  to a new git repo using gh


First, let's initialize the git repository and make the initial commit:

```
git init && git add . && git commit -m "Initial commit: Stock price movement and news analyzer"
```


Install gh if its not installed already. On mac, you use brew install.


This will create a remote repo and push your local code to its main branch : 


```
gh repo create big_moves --public --description "A Python tool for analyzing significant stock price movements and correlating them with news events" --source=. --remote=origin --push
```
