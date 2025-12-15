# RolePlayingBot


This bot was used to help manage a "Westmarch D&D Campaign", an open-to-all Dungeons and Dragons group with multiple game masters where you sign up for individual sessions, or "quests", only when you have time with no weekly commitments. 

The bot managed quest listings, sending out announcements and notifications to players and game masters related to quests they were a part of, as well as keeping track of characters and their in-game resources. Information was stored and updated in a SQL cloud database, and was accessed/updated using PHP commands from a Node.js library.

This bot was one of my earliest major programming projects, so while there are many places where code is not best-practice (ex: app is one big code file instead of being split by function), it still shows a familiarity of working with a SQL cloud database through an API, with permission structure and user input error checking. 

### Database functionality:

- Tracking characters examples:
    - adding new entry to database (app.js:  line 1970, 2040)
    - selecting and editing multiple entries (app.js: line 2219 - select; line 2258 - update)
    - accessing and displaying data (app.js: line 2557)
- Tracking task ("quests") listings examples:
    - creating new posting (app.js: line 1552; line 1630 - insert into database)
    - update task status (app.js: line 1429 - select; line 1455 - update)
    - access and display task list (app.js: line 1509-1550)
    - archive completed tasks (app.js: line 2112-2217)

### Other functionality

- regex parsing: used regex extensively to parse command inputs. Examples: (app.js: line 793), (app.js: line 1568)
- Reading and parsing JSON dataset
    - load in JSON (app.js: line 51-66)
    - parse and use JSON objects (app.js: line 1914-1953)