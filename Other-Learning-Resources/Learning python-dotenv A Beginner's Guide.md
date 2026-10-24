# Learning python-dotenv: A Beginner's Guide

Oct 24, 2026 · @paul

## 1. Reading the line

`from dotenv import load_dotenv` means: from the `dotenv` module, bring the `load_dotenv` function into this file so I can call it.

| Word | Meaning |
| --- | --- |
| `from` | Python keyword: "take something out of a module" |
| `dotenv` | The module (a library someone else wrote) you are borrowing from |
| `import` | Python keyword: "make it available in my file" |
| `load_dotenv` | A function inside `dotenv` that reads a `.env` file |

After this line you can write `load_dotenv()`. That one call reads a file named `.env` in your project and loads each line in it as an environment variable your program can read.

The import line on its own does nothing visible. Only calling `load_dotenv()` does the work.

## 2. The problem dotenv solves

dotenv lets you keep secrets and settings (API keys, passwords, database URLs) in a separate `.env` file instead of typing them into your code.

Without it, beginners often write this:

```python
api_key = "sk-abc123-my-real-secret"   # bad: anyone who sees the code sees the key
```

If you share that file or push it to GitHub, your key leaks. Bots scan GitHub for leaked keys within minutes.

**Environment variables** are named values that live outside your program, in the operating system. Every program can read them. For example, `PATH` and `HOME` are environment variables your computer already has.

Setting them by hand in the terminal every time is tedious. dotenv fixes that:

1. You write your settings once in a plain text file called `.env`.
2. Your script calls `load_dotenv()`.
3. dotenv copies each line of `.env` into the environment variables.
4. Your code reads them with `os.getenv("NAME")`.

The code stays clean and shareable; the secrets stay in one private file. This idea comes from the "Twelve-Factor App" practice of storing config in the environment.

## 3. Installing it

dotenv is not built into Python, so install it once with pip:

```bash
pip install python-dotenv
```

**Watch out:** the package you install is `python-dotenv`, but the module you import is `dotenv`. Running `pip install dotenv` installs a different, unrelated package and causes confusing errors.

| You type | Where |
| --- | --- |
| `pip install python-dotenv` | Terminal / command prompt |
| `from dotenv import load_dotenv` | Your `.py` file |

If you use a virtual environment (recommended), activate it before running pip. On some systems the command is `pip3` or `python -m pip install python-dotenv`.

Check it worked:

```bash
python -c "import dotenv; print('dotenv is installed')"
```

**Version check:** the latest release is 1.2.4 (1 October 2026), and it needs **Python 3.10 or newer**. Run `python --version` to see yours.

Want the optional `dotenv` command-line tool too (section 11)? Install the `cli` extra instead; the quotes matter in some shells:

```bash
pip install "python-dotenv[cli]"
```

## 4. Your first .env file and script

Three files, five minutes. Make a folder, e.g. `dotenv_demo`, and put these inside.

**Step 1 — create a file named exactly `.env`** (starts with a dot, no name before it, no `.txt` after it):

```bash
# .env
APP_NAME=My First App
API_KEY=sk-test-12345
DEBUG=True
MAX_USERS=50
```

Rules: one `KEY=value` per line; lines starting with `#` are comments. Spaces around `=` are ignored, but `KEY=value` with no spaces is the usual style. Full syntax is in section 8.

**Step 2 — create `main.py` in the same folder:**

```python
import os
from dotenv import load_dotenv

load_dotenv()  # reads .env and sets the variables

app_name = os.getenv("APP_NAME")
api_key = os.getenv("API_KEY")

print("App:", app_name)
print("Key starts with:", api_key[:7])
```

**Step 3 — run it:**

```bash
python main.py
```

Expected output:

```text
App: My First App
Key starts with: sk-test
```

**Try this:** comment out the `load_dotenv()` line and run again. `app_name` becomes `None`, and `api_key[:7]` crashes. That shows exactly what `load_dotenv()` does.

## 5. Reading values

Use `os.getenv` for optional settings and `os.environ[...]` for required ones; remember every value comes back as text.

| Way to read | Missing variable gives | Use for |
| --- | --- | --- |
| `os.getenv("NAME")` | `None` | Optional settings |
| `os.getenv("NAME", "default")` | `"default"` | Optional settings with a fallback |
| `os.environ["NAME"]` | `KeyError` crash | Required settings — fail loudly early |

```python
import os
from dotenv import load_dotenv

load_dotenv()

port = os.getenv("PORT", "8000")     # optional, falls back to "8000"
api_key = os.environ["API_KEY"]       # required, crash if missing
```

**Everything is a string.** `.env` is a text file, so `MAX_USERS=50` arrives as `"50"`, not the number 50. Convert it yourself:

```python
max_users = int(os.getenv("MAX_USERS", "10"))     # "50" -> 50
rate = float(os.getenv("RATE", "0.5"))            # "0.5" -> 0.5
debug = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
```

Beware: `bool("False")` is `True` in Python (any non-empty string is true). That's why the `debug` line compares text instead.

## 6. Useful options

Most projects only ever need `load_dotenv()`; these extras cover the next few situations you'll hit.

**Override existing variables.** By default, `load_dotenv()` does not replace a variable that is already set in your system. To make `.env` win:

```python
load_dotenv(override=True)
```

**Load a file from somewhere else** (or with a different name):

```python
load_dotenv(dotenv_path="config/dev.env")
```

**Searching parent folders happens automatically.** Plain `load_dotenv()` already calls `find_dotenv()`, which starts in the folder of your script and walks up. Call `find_dotenv()` yourself only to change how it searches (section 7):

```python
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(usecwd=True))   # search from the current working folder instead
```

**Read into a dictionary without touching the environment:**

```python
from dotenv import dotenv_values
config = dotenv_values(".env")   # {'APP_NAME': 'My First App', ...}
print(config["APP_NAME"])
```

**Check whether anything loaded.** `load_dotenv()` returns `True` if it set at least one variable, `False` otherwise.

### .env file syntax

```bash
# Comments start with #
NAME=Asha
GREETING="Hello world"          # quotes keep spaces
BASE_URL=https://api.example.com
USERS_URL=${BASE_URL}/users      # reuse another variable (braces required)
export TOKEN=abc                 # 'export' prefix is allowed
PRIVATE_KEY="line one
line two"                        # multi-line value inside quotes
```

Sections 8 and 9 cover every syntax rule and variable expansion in detail.

**Also available:** `verbose`, `interpolate`, `encoding` and `stream` options (section 10), and a command-line tool (section 11).

## 7. How load\_dotenv finds your .env

With no arguments, `load_dotenv()` looks for `.env` in the folder of the script that called it, then in each parent folder up to the top of the drive.

Two exceptions: in Jupyter, the Python REPL, a debugger, or a frozen app (e.g. PyInstaller), there is no script file, so the search starts from the **current working folder** instead.

If nothing is found, `load_dotenv()` quietly does nothing and returns `False`. Pass `verbose=True` to get a warning instead.

`find_dotenv()` options:

| Parameter | Default | What it does |
| --- | --- | --- |
| `filename` | `".env"` | Name of the file to search for, e.g. `".env.dev"` |
| `raise_error_if_not_found` | `False` | Raise `IOError` instead of returning `""` |
| `usecwd` | `False` | Start from the current working folder, not the script's folder |

```python
from dotenv import load_dotenv, find_dotenv

# Fail loudly if .env.dev is missing anywhere up the tree
load_dotenv(find_dotenv(".env.dev", raise_error_if_not_found=True))
```

## 8. The .env file format in depth

A `.env` file looks mostly like a Bash file; the format has no formal spec, so these are the rules python-dotenv follows.

| Rule | Example | Result |
| --- | --- | --- |
| Spaces around key, `=` and value are ignored | `NAME = Asha` | `"Asha"` |
| Values may be unquoted, `'single'` or `"double"` quoted | `MSG="Hi there"` | `"Hi there"` |
| Keys may be unquoted or single-quoted | `'MY_KEY'=1` | key `MY_KEY` |
| `#` starts a comment only after a space | `COLOR=red #note` | `"red"` |
| `#` with no space before it is part of the value | `COLOR=red#1` | `"red#1"` |
| `export` prefix is ignored | `export PORT=8000` | `"8000"` |
| Quoted values can span lines | see below | text with a line break |
| Key with no `=` | `FOO` | ignored by `load_dotenv`; `None` in `dotenv_values` |
| Key with empty value | `FOO=` | `""` (empty string) |

**Escape sequences** (a backslash plus a letter):

- Single-quoted values understand only `\\` and `\'`.
- Double-quoted values also understand `\"`, `\n` (new line), `\t` (tab), `\r`, `\a`, `\b`, `\f` and `\v`.

**Multi-line values.** These two are identical:

```bash
FOO="first line
second line"
```

```bash
FOO="first line\nsecond line"
```

On Unix, python-dotenv can also read from a named pipe (FIFO) instead of a regular file.

## 9. Variable expansion

A value can reuse another variable with `${NAME}`; the braces are required, because a bare `$NAME` is left as plain text.

```bash
DOMAIN=example.org
ADMIN_EMAIL=admin@${DOMAIN}        # admin@example.org
ROOT_URL=${DOMAIN}/app             # example.org/app
WRONG=$DOMAIN/app                  # stays "$DOMAIN/app" (no braces)
LOG_LEVEL=${LEVEL:-info}           # "info" if LEVEL is not set anywhere
```

**Where the value comes from.** When `${NAME}` is expanded, python-dotenv takes the first of these that exists:

| Order | `load_dotenv()` (default, `override=False`) | `load_dotenv(override=True)` or `dotenv_values()` |
| --- | --- | --- |
| 1st | Your system environment | The `.env` file |
| 2nd | The `.env` file | Your system environment |
| 3rd | The default after `:-` | The default after `:-` |
| 4th | Empty string | Empty string |

**Turn expansion off** when your values contain a literal `${...}` (some passwords do):

```python
load_dotenv(interpolate=False)
```

## 10. More ways to load

Beyond a single `.env` file, python-dotenv can merge several files, read from text in memory, run inside Jupyter, and be switched off.

**Full `load_dotenv` signature** (all optional):

| Parameter | Default | What it does |
| --- | --- | --- |
| `dotenv_path` | `None` | Path to the file; `None` means search with `find_dotenv()` |
| `stream` | `None` | A text stream (e.g. `StringIO`) to read instead of a file |
| `verbose` | `False` | Warn if the `.env` file is missing |
| `override` | `False` | Let `.env` values replace existing system variables |
| `interpolate` | `True` | Expand `${VAR}` references |
| `encoding` | `"utf-8"` | Text encoding used to read the file |

`dotenv_values()` takes the same parameters except `override`.

**Merge several files into one config dict.** Later entries win, so real environment variables override both files:

```python
import os
from dotenv import dotenv_values

config = {
    **dotenv_values(".env.shared"),   # shared, non-secret settings
    **dotenv_values(".env.secret"),   # private secrets
    **os.environ,                     # real environment wins
}
```

**Load from text instead of a file**, e.g. settings fetched over the network:

```python
from io import StringIO
from dotenv import load_dotenv

load_dotenv(stream=StringIO("USER=foo\nEMAIL=foo@example.org"))
```

**Jupyter / IPython.** Load the extension once, then use the magic command:

```python
%load_ext dotenv
%dotenv                      # searches for .env
%dotenv path/to/other.env    # or a specific file
%dotenv -o -v                # -o override, -v verbose
```

**Switch it off without touching code.** Set the environment variable `PYTHON_DOTENV_DISABLED=1` and every `load_dotenv()` call does nothing and returns `False`. Useful in production, or when a library you can't edit calls `load_dotenv()`.

## 11. The dotenv command line

The optional `dotenv` command lets you view and edit `.env` from the terminal, and run any program with it loaded. Install it with `pip install "python-dotenv[cli]"`.

| Command | What it does |
| --- | --- |
| `dotenv set USER foo` | Add or update a key (creates `.env` if missing) |
| `dotenv get USER` | Print just the value |
| `dotenv unset USER` | Remove a key |
| `dotenv list` | Print all `KEY=value` pairs |
| `dotenv list --format=json` | Print them as JSON |
| `dotenv run -- python app.py` | Run a program with `.env` loaded |
| `dotenv run --no-override -- python app.py` | Same, but existing system variables win |

Useful options go before the command: `-f path/to/file.env` picks a different file, and `-q always|auto|never` controls quoting when `set` writes a value. `python -m dotenv ...` works too if the `dotenv` command isn't on your PATH. Run `dotenv --help` for the full list.

```bash
$ dotenv set EMAIL foo@example.org
$ dotenv list --format=json
{
  "EMAIL": "foo@example.org"
}
```

`dotenv run` is handy for non-Python programs, or for Python code that never calls `load_dotenv()`.

## 12. Reading and editing .env from Python

Three functions read or change a single key directly in the file, without loading anything into the environment.

```python
from dotenv import get_key, set_key, unset_key

set_key(".env", "THEME", "dark")       # adds THEME='dark' (creates .env if missing)
print(get_key(".env", "THEME"))         # dark
unset_key(".env", "THEME")              # removes the line
```

| Function | Returns | Notes |
| --- | --- | --- |
| `get_key(path, key)` | The value, or `None` if the key is missing or has no value | Reads one key |
| `set_key(path, key, value)` | `(True, key, value)` | `quote_mode="always"` (default), `"auto"` or `"never"`; `export=True` writes an `export` prefix |
| `unset_key(path, key)` | `(True, key)`, or `(None, key)` with a warning if the file or key is missing | Removes one key |

These write to the file only. To use the new value in the running program, call `load_dotenv(override=True)` again. For safety, `set_key` and `unset_key` don't follow symbolic links unless you pass `follow_symlinks=True`.

## 13. Keeping secrets safe

The whole point of `.env` is privacy, so never commit it to Git; share a `.env.example` instead.

1. **Ignore `.env` in Git.** Add this line to a file named `.gitignore` in your project root:

   ```text
   .env
   ```
2. **Commit a `.env.example` template** with the same keys and fake values, so teammates know what to fill in:

   ```bash
   # .env.example — copy to .env and fill in real values
   API_KEY=your-api-key-here
   DEBUG=False
   ```
3. **If you leaked a key, revoke it.** Deleting it from Git is not enough; old commits keep it. Generate a new key on the provider's website.
4. **In production, skip the file.** Hosting platforms (Heroku, Render, AWS, GitHub Actions secrets, Docker) let you set environment variables in their dashboard. Your code still calls `os.getenv`, and `load_dotenv()` simply finds no file and changes nothing.
5. **Never print full secrets** in logs. Print only the first few characters, as in section 4.

## 14. Common mistakes and fixes

Most dotenv bugs are a wrong file name, a wrong folder, or a forgotten `load_dotenv()` call.

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `ModuleNotFoundError: No module named 'dotenv'` | Package not installed, or installed in a different Python | `pip install python-dotenv` in the same environment you run with |
| Strange errors after `pip install dotenv` | Installed the wrong package | `pip uninstall dotenv`, then `pip install python-dotenv` |
| `os.getenv(...)` returns `None` | `load_dotenv()` not called, or called after reading | Call `load_dotenv()` near the top, before any `os.getenv` |
| Still `None` | File saved as `.env.txt` (common on Windows) | Turn on "File name extensions" in Explorer and rename to `.env` |
| Still `None` | `.env` is not in the script's folder or any parent folder | Move it, or pass the full path: `load_dotenv("/full/path/.env")` |
| Still `None` in Jupyter or the REPL | There the search starts from the current working folder | Check `os.getcwd()`, or pass the full path |
| Nothing loads anywhere | `PYTHON_DOTENV_DISABLED` is set | Unset it; check that `load_dotenv()` returns `True` |
| Old value keeps showing | Variable already set in your system | `load_dotenv(override=True)` |
| Part of a value vanished or changed | An unquoted value contains `  # ` (read as a comment) or `${...}` (expanded) | Wrap the value in quotes, or use `interpolate=False` |
| `$NAME` appears literally in a value | Bare `$NAME` is not expanded | Use `${NAME}` |
| `TypeError` doing math with a value | Values are strings | Wrap in `int()` or `float()` |

Quick debug snippet:

```python
import os
from dotenv import load_dotenv, find_dotenv

path = find_dotenv()
print("Found .env at:", path or "NOT FOUND")
print("Loaded anything?", load_dotenv(path))
print("API_KEY set?", "API_KEY" in os.environ)
```

## 15. Practice and cheat sheet

Work through these in order; each builds on the demo from section 4.

- [ ] Add `CITY=Bengaluru` to `.env` and print a greeting that uses it.
- [ ] Read `MAX_USERS` as a number and print `MAX_USERS * 2`.
- [ ] Read `DEBUG` as a real `True`/`False` and print "Debug mode on" only when it's true.
- [ ] Make `API_KEY` required with `os.environ[...]`, delete it from `.env`, and see the error.
- [ ] Create `.gitignore` and `.env.example` for the demo folder.
- [ ] Create `dev.env` and `prod.env` with different `APP_NAME` values; load one with `dotenv_path=`.
- [ ] Use `dotenv_values()` to print every key in `.env` without loading them.
- [ ] Add `BASE_URL` and `USERS_URL=${BASE_URL}/users`; print `USERS_URL`. Then try `$BASE_URL` without braces.
- [ ] Use `${LEVEL:-info}` and run once with `LEVEL` unset, once with it set in your terminal.
- [ ] Use `set_key` to save a `LAST_RUN` timestamp each time your script runs.
- [ ] Install the CLI and try `dotenv list --format=json` and `dotenv run -- python main.py`.

### Cheat sheet

```python
# Terminal:  pip install python-dotenv        (Python 3.10+)
#            pip install "python-dotenv[cli]" (adds the dotenv command)

import os
from dotenv import (load_dotenv, find_dotenv, dotenv_values,
                    get_key, set_key, unset_key)

load_dotenv()                         # search script folder, then parents
load_dotenv("path/to/file.env")       # specific file
load_dotenv(override=True)            # .env beats system variables
load_dotenv(interpolate=False)        # don't expand ${VAR}
load_dotenv(verbose=True)             # warn if .env is missing
load_dotenv(find_dotenv(usecwd=True)) # search from current working folder

os.getenv("KEY")                      # str or None
os.getenv("KEY", "default")           # str with fallback
os.environ["KEY"]                     # str, KeyError if missing
int(os.getenv("NUM", "0"))            # convert to number

dotenv_values(".env")                 # dict, environment untouched
set_key(".env", "K", "v")             # write one key to the file
get_key(".env", "K")                  # read one key from the file
unset_key(".env", "K")                # delete one key from the file

# .env:  URL=${HOST}/api   LEVEL=${LEVEL:-info}   export PORT=8000
# Shell: PYTHON_DOTENV_DISABLED=1 turns load_dotenv() off
```

**Related tools** (listed by the python-dotenv project) for when you outgrow it: [environs](https://github.com/sloria/environs) adds type conversion and validation; [python-decouple](https://github.com/HBNetwork/python-decouple), [dynaconf](https://github.com/dynaconf/dynaconf) and [django-environ](https://github.com/joke2k/django-environ) handle bigger configuration setups.

## Sources

- [python-dotenv documentation](https://saurabh-kumar.com/python-dotenv/) (official docs site)
- [python-dotenv API reference](https://saurabh-kumar.com/python-dotenv/reference/)
- [python-dotenv on PyPI](https://pypi.org/project/python-dotenv/) (version 1.2.4, changelog)
- [python-dotenv on GitHub](https://github.com/theskumar/python-dotenv)
