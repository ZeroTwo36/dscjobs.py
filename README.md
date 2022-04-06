# dscjobs.py

A modern, easy to use, feature-rich ready API wrapper for DSCJobs written in Python.

## Installation

On Linux and MacOS, these commands shall suffice: 
```sh
pip3 install -U git+https://github.com/ZeroTwo36/dscjobs.py.git
```
While on Win32 Systems, it's like 
```cmd
pip install -U git+https://github.com/ZeroTwo36/dscjobs.py.git
```

## A Very, very basic Example - Pull your own Stats

Now watch this, I'll pull my own DSCJobs Stats!

```py
from dscjobs import fetchUser
myself = 899722893603274793
user = fetchUser(myself)
print(f"Premium: {user.premium}\nStaff: {user.staff}")
exit()
```

