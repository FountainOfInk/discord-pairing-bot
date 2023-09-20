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

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
