# [old] Legendarium Bot

This is a chat bot I wrote and maintain for the Discord server of The Legendarium Podcast. The original version was made in 2017 as one of my first major projects when I was first learning to code, but I have since rewritten it from the ground up using updated API and best practices I learned since then. 

An overview of some of the relevant features of the bot are:

- Automated messaging and tasks
    - timed cron alerts (index.js: line 131, 169)
    - member join message (index.js: line 235)
    - search for and post new podcast episodes using API, and parsing API data with regex (functions/init.js: line 59 -> calls functions/updateXML.js -> calls functions/spotify-update.js)
    - \[deprecated in favor of Spotify API\] web scraping and parsing XML file (functions/searchForXMLupdates.js) 
- User commands
    - multi-parameter commands to execute a variety of tasks, or modify/override automated tasks through Discord API Slash Commands (list of commands in commands sub-folder)
    - \[deprecated in favor of Slash Commands\] read and execute commands from text message inputs (index.js: line 252 -> calls functions/message-command.js)
    - Note tracking / personal reminder to keep track of important messages (index.js: line 311 -> calls functions/reminder.js)
- Local JSON data storage to keep track of relevant information for the bot (memory.json; bot-constants.json)
- Developer mode to test updates and changes in testing environment without disruption of service (bot-constants.json `TESTING_MODE` flag, activates testing environment)


