# Removing secrets from git history

The scenario here is, you have a secret in your commit history and push to origin errored out because of it. 
Now you need to remove the offending file from your local git history.


```bash
brew install git-filter-repo

git filter-repo --path .env --invert-paths --force

git remote add origin https://github.com/pbprasad99/big_moves.git

git push --set-upstream origin main 

git push origin --force --all 
```

## Additional Reference :

https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
