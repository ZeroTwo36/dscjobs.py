# dscjobs.py

A modern, easy to use, feature-rich, and async ready API wrapper for DSCJobs written in Python.

## Installation

On Linux and MacOS, these commands shall suffice: 
```sh
pip3 install -U git+https://github.com/ZeroTwo36/dscjobs.py.git
```
While on Win32 Systems, it's like 
```cmd
pip install -U git+https://github.com/ZeroTwo36/dscjobs.py.git
```

## A Very, very basic Example with asyncio

Now watch this, I'll pull my own DSCJobs Stats!

```py
from dscjobs import fetchUser
import asyncio

def main():
  myself = 899722893603274793
  user = await fetchUser(myself)
  print(f"Premium: {user.premium}\nStaff: {user.staff}")
  exit()
 asyncio.run(main())
```

I can also fetch Reviews, look:
```py
from dscjobs import fetchReview
import asyncio

def main():
  myself = 899722893603274793
  rev = await fetchReview(myself)
  print(f"Review: {rev.content}\nRate: {rev.rate}")
  exit()
 asyncio.run(main())

```

# Upcoming/Planned:
* Converting the core.User object to a discord.User() so it has more features  
* Handle Vanity URLs (/user/ZeroTwo36 to /user/899722893603274793 for example)  
