# Minecraft Block Entity Invalid Fixer
After a server/game crash minecraft worlds can get scrambled. After manually moving chunks back
using a tool like [MCA Selector](https://github.com/Querz/mcaselector), there still can be issues with chests, barrels, etc.

When that is the case, typically the following message will show (when running a server):
```
[15:31:33] [Server thread/WARN]: Block entity invalid: minecraft:chest @ BlockPosition{x=-109, y=69, z=-162}
```

This script is able to fix (some of) these issues.

### Usage
Make sure you have python 3 installed. (This script was made for 3.8 but other versions might work too)

1. Clone this repo.
2. Open this directory in a terminal
3. Run `pip3 install -r requirements.txt`
4. Run `python3 entityfixer.py [path-to-your-minecraft-world]`

Make sure you create a backup of your world before trying this.

