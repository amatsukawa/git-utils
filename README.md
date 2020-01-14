# git-utils

This is a reimplementation of a subset of functionality in [`scm_breeze`](https://github.com/scmbreeze/scm_breeze).

## Why not just use `scm_breeze`?

The simple answer is security. `scm_breeze` has so much functionality that I could not possibly personally
audit every line, and every update, to see what it's doing. For that reason, I've resisted using it at work,
Of course it's not that I am suspicious of `scm_breeze` repo owners specifically, it's just general paranoia.
Stuff like [this](https://www.theregister.co.uk/2018/11/26/npm_repo_bitcoin_stealer/) is not unheard of.

## Installation

Just as I'm uneasy about `scm_breeze`, unless you know me personally, I'd expect you to be uneasy about using
this utility also. Instructions are more for me to copy paste when I sit down at a new setup.
If you want, feel free to use it.

This implementation is much shorter than `scm_breeze` because it only has a subset of its functionality. It's also
in python, which is much more readable IMHO. So you could read the ~250 lines or so and see what it's doing, if you
were so inclined.

I wrote this over a Saturday. There are no tests, only me testing it at my terminal.
I expect it to have bugs. If it breaks your git repo, I take no responsibility.
```
git clone https://github.com/amatsukawa/git-utils.git ~/.git-utils
echo 'export GIT_UTILS_ROOT="${HOME}/.git-utils"' >> ~/.zshrc
echo 'export GIT_UTILS_CACHE="${HOME}/.git_utils_cache"' >> ~/.zshrc
echo 'export GIT_UTILS_PYTHON=python' >> ~/.zshrc
echo 'export PATH=$PATH:${GIT_UTILS_ROOT}/bin' >> ~/.zshrc
echo 'source ${GIT_UTILS_ROOT}/aliases.sh' >> ~/.zshrc

```

