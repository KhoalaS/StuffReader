# StuffReader

Manga/Comic/Webtoon reader but in python.

Focusing on extensibility.

Extensions for a specific site need to implement some of the methods of the `Extension` class in `lib/extension.py`.

These extensions can then be registered in the `main.py`

```py
from extensions import my_extension

# ... other code

con = sqlite3.connect("./data.db")

registry = Registry()
registry.register(my_extension.Ext(con))
# ... other code
```

# Usage

Coming after MVP

## Docker

# Build

Coming after MVP
