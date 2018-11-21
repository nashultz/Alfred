[![PyPI](https://img.shields.io/badge/discord.py-1.0.0a-green.svg)](https://github.com/Rapptz/discord.py/tree/rewrite/)
[![PyPI](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-364/)
[![PyPI](https://img.shields.io/badge/support-discord-lightgrey.svg)]()

# Alfred
A Discord helper bot for Pokemon Go communities.

Alfred is a Discord bot written in Python 3.6.1+ built with [discord.py v1.0.0a (rewrite branch)](https://github.com/Rapptz/discord.py/tree/rewrite)

## Alfred v0.0.1 Features

Alfred assists with organizing Pokemon Go communities with support for:

 - Team assignments
 - Server greetings
 - Wild Pokemon reporting
 - Raid reporting and RSVP
 - Research reporting
 - Pokebattler integration for raid counters
 - Silph card integration
 - Gym matching extension for self-hosters

#### *`Note: All reports are provided by your active server members. Alfred does not support any TOS breaking features such as spoofing, Pokemon Go bot accounts and automated raid reporting.`*

# Invite Public Alfred (no hosting required)


1. Use [THIS LINK](https://discordapp.com/oauth2/authorize?client_id=512045813434941442&scope=bot&permissions=268822608) to invite Alfred  
1. Select your server and click Authorize
1. Verify you aren't a robot (if the captcha doesn't appear, disable your adblocker)
1. In your server, type `!configure`
1. Go through the DM configuration session with Alfred to setup your server  
   *Be sure to read the prompts carefully!*
1. That's it! Enjoy!

#### *``Note: You must have the manage_server permission to invite a bot.``*

## Directions for using Alfred:
Note: Avoid punctuation inside commands.

Arguments within \< \> are required.<br/>
Arguments within \[ \] are optional.<br/>
pkmn = Pokemon

### Admin or Manager Commands:

| Commands | Requirements  | Description |
| -------- |:-------------:| ------------|
| **!save**  | *Owner Only* | Saves the save data to file. |
| **!exit**  | *Owner Only* | Saves the save data to file and shutdown Alfred. |
| **!restart**  | *Owner Only* | Saves the save data to file and restarts Alfred. |
| **!announce** \[msg\] | *Owner Only* | Sends announcement message to server owners. |
| **!welcome** \[@member\] | *Owner Only* | Sends the welcome message to either user or mentioned member. |
| **!outputlog**  | *Server Manager Only* | Uploads the log file to hastebin and replies with the link. |
| **!set prefix** \[prefix\] | *Server Manager Only* | Sets Alfred's prefix. |
| **!set regional** \<pkmn\> | *Server Manager Only* | Sets server's regional raid boss. Accepts number or name. |
| **!set timezone** \<UTC offset\> | *Server Manager Only* | Sets server's timezone. Accepts numbers from -12 to 14. |
| **!get prefix** | *Server Manager Only* | Displays Alfred's prefix. |
| **!get perms** \[channelid\] | *Server Manager Only* | Displays Alfred's permissions in guild and channel. |
| **!welcome** \[user\] | *Owner Only* | Test welcome message on mentioned member |
| **!configure** | *Server Manager Only* | Configure Alfred |
| **!reload_json** | *Owner Only* | reloads JSON files for the server |
| **!raid_json** \[level\] \[bosslist\] | *Owner Only* | Edits or displays raid_info.json |
| **!changeraid** \[level or boss\] | *Channel Manager Only* | Changes raid boss or egg level |
| **!clearstatus**  | *Channel Manager<br/>Raid Channel* | Cancel everyone's status. |
| **!setstatus** \<user\> \<status\> \[count\] | *Channel Manager<br/>Raid Channel* | Changes raid channel status lists. |
| **!cleanroles** | *Channel Manager* | Removes all 0 member pokemon roles. |
| **!reset_board** \[user\] \[type\] | *Server Manager* | Resets \[user\]'s or server's leaderboard by type or total. |

### Miscellaneous Commands
| Commands | Requirements  | Description |
| -------- |:-------------:| ------------|
| **!help** \[command\] | - | Shows bot/command help, with descriptions. |
| **!about** | - | Shows info about Alfred. |
| **!uptime** | - | Shows Alfred's uptime. |
| **!team** \<team\> | - | Let's users set their team role. |
| **!set silph** \<Silph name\> | - | Links user\'s Silph Road account to Alfred. |
| **!silphcard** \[Silph name\] | - | Displays [Silph name]\'s or user\'s trainer card. |
| **!profile** \[username\] | - | Displays [username]\'s or user\'s profile. |
| **!leaderboard** \[type\] | - | Displays reporting leaderboard. Accepts total, raids, eggs, exraids, wilds, research. Defaults to total. |

### Pokemon Notification Commands:

| Commands | Requirements  | Description |
| -------- |:-------------:| ------------|
| **!want** \<pkmn\> | *Want Channel* | Adds a Pokemon to your notification roles. |
| **!unwant** \<pkmn\> | *Want Channel* | Removes a Pokemon from your notification roles. |
| **!unwant all**  | *Want Channel* | Removes all Pokemon from your notification roles. |

### Reporting Commands:

| Commands | Requirements  | Description |
| -------- |:-------------:| ------------|
| **!wild** \<pkmn\> \<location\> | *Region Channel* | Reports a wild pokemon, notifying people who want it. `Aliases: !w` |
| **!raid** \<pkmn\> \<place\> \[timer\] | *Region Channel* | Creates an open raid channel. `Aliases: !r`|
| **!raidegg** \<level\> \<place\> \[timer\] | *Region Channel* | Creates a raid egg channel. `Aliases: !re, !regg, !egg` |
| **!raid** \<pkmn\> | *Raid Egg Channel* | Converts raid egg to an open raid. |
| **!raid assume** \<pkmn\> | *Raid Egg Channel* | Assumes a pokemon on hatch. |
| **!exraid** \<pkmn\> \<place\> | *Region Channel* | Creates an exraid channel. `Aliases: !ex`|
| **!invite**  | *Region Channel* | Gain entry to exraids. |
| **!research** \[pokestop name \[optional URL\], quest, reward\] | *Region Channel* | Reports field research. Guided version available with just **!research** `Aliases: !res` |

### Raid Channel Management:

| Commands | Requirements  | Description |
| -------- |:-------------:| ------------|
| **!timer** | *Raid Channel* | Shows the expiry time for the raid. |
| **!timerset** \<timer\> | *Raid Channel* | Set the expiry time for the raid. |
| **!starttime** \[HH:MM AM/PM\] | *Raid Channel* | Set a time for a group to start a raid. |
| **!location** | *Raid Channel* | Shows the raid location. |
| **!location new** \<place/map\> | *Raid Channel* | Sets the raid location. |
| **!recover** | *Raid Channel* | Recovers an unresponsive raid channel. |
| **!duplicate** | *Raid Channel* | Reports the raid as a duplicate channel. |
| **!weather** | *Raid Channel* | Sets the weather for the raid. |
| **!counters** | *Raid Channel* | Simulate a Raid battle with Pokebattler. |
| **!archive** | *Raid Channel* | Mark a channel for archiving. |

### Status Management:

| Commands | Requirements  | Description |
| -------- |:-------------:| ------------|
| **!interested** \[number\] \[teamcounts\] \[boss list or all\] | *Raid Channel* | Sets your status for the raid to 'interested'. Teamcounts format is `m# v# i# u#`. You can also supply a list of bosses or 'all' that you are interested in. `Aliases: !i, !maybe` |
| **!coming** \[number\] \[teamcounts\] \[boss list or all\] | *Raid Channel* | Sets your status for the raid to 'coming'.  Teamcounts format is `m# v# i# u#`. You can also supply a list of bosses or 'all' that you are interested in. `Aliases: !c` |
| **!here** \[number\] \[teamcounts\] \[boss list or all\] | *Raid Channel* | Sets your status for the raid to 'here'.  Teamcounts format is `m# v# i# u#`. You can also supply a list of bosses or 'all' that you are interested in. `Aliases: !h` |
| **!lobby** \[number\] | *Raid Channel* | Indicate you are entering the raid lobby. `Aliases: !l` |
| **!starting** \[team\] | *Raid Channel* | Clears all members 'here', announce raid start. |
| **!backout** | *Raid Channel* | Request players in lobby to backout. |
| **!cancel**  | *Raid Channel* | Cancel your status. `Aliases: !x` |

### List Commands:

| Commands | Requirements  | Description |
| -------- |:-------------:| ------------|
| **!list** | *Region Channel* | Lists all raids from that region channel. `Aliases: !lists`|
| **!list**  | *Raid Channel* | Lists all member status' for the raid. `Aliases: !lists`|
| **!list tags** | *Raid Channel* | Same behavior as !list, but with @mentions. |
| **!list interested** | *Raid Channel* | Lists 'interested' members for the raid. |
| **!list coming**  | *Raid Channel* | Lists 'coming' members for the raid. |
| **!list here** | *Raid Channel* | Lists 'here' members for the raid. |
| **!list lobby** | *Raid Channel* | List the number and users who are in the raid lobby. |
| **!list teams** | *Raid Channel* | Lists teams of the members that have RSVPd. |
| **!list mystic** | *Raid Channel* | Lists teams of mystic members that have RSVPd. |
| **!list valor** | *Raid Channel* | Lists teams of valor members that have RSVPd. |
| **!list instinct** | *Raid Channel* | Lists teams of instinct members that have RSVPd. |
| **!list unknown** | *Raid Channel* | Lists members with unknown team that have RSVPd. |
| **!list bosses** | *Raid Channel* | Lists boss interest of members that have RSVPd. |
| **!list wants** | *Want Channel* | List the wants for the user. |
| **!list wilds** | *Region Channel* | List the wilds for the channel. |
| **!list research** | *Region Channel* | List the research for the channel. |

## General notes on Alfred:

Alfred relies completely on users for reports. Alfred was designed as an alternative to Discord bots that use scanners and other illegitimate sources of information about Pokemon Go. As a result, Alfred works only as well as the users who use it. As there are a lot of ways to interact with Alfred, there can be a bit of a rough learning period, but it quickly becomes worth it. Some commands are not necessary for normal usage and are only there for advanced users.
