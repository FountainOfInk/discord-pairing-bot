# Discord Pairing Bot

This is a Discord bot that pairs 2 given people together, based on preferences such as age, gender, and location.
`py-cord` is used for the bot library. No other external python libraries are used.

### Usage:
0. Change the values in `constant_config.py` to reflect your guild.
1. Someone recieves the roles for themselves, (ex: They ask for a role that specifies they are from Europe.) and some roles for the people they wish to be paired with (ex: They ask for a role that specifies to only be matched with males.)
2. They run the "slash command" `/please_pair_me`. This adds them to a pool, which periodically checks for people who are compatible with each other, (A must be ok with all of B's attributes, and vice versa.) and pairs them (makes a private category with a private voice and text chat for both members.)

### Extending:
There are some utilities provided in `debugging.py` to facilitate further development. Be sure to set `TESTING` to `True` in `constant_config.py`.


Note:

    discord-pairing-bot pairs discord users in private channels together based on various attributes.
    Copyright (C) 2023 FountainOfInk

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
