
# Task List

1. implement bot.TESTING_MODE everywhere
1. ~~commenting everywhere~~
1. ~~confirm async/await everywhere~~
1. make /endseries an autocomplete option for series name
1. make /postepisode series better
  - ~~"series_thread" solely determines if its posted in a series or not~~
    - ~~not including the optional means its not posted in series~~
  - ~~remove "post_series" option~~
  - add WARNING that notes the episode was identified in series but wasnt posted
    - or if it is being posted in the wrong series
1. manual-post.js
  - make button-response more robust 
    - [give it its own interaction]
    - OR put message saying if it doesn't repsond, try again
  - fix bugged reply text for options
1. ~~updateXML.js~~
  - make button-response more robust 
    - [give it its own interaction]
    - OR put message saying if it doesn't repsond, try again



# implement bot.TESTING_MODE procedures
- context-menu
- ~~end_series~~
- make_series
- ~~show_active_series~~
- stored-episodes
- ~~suggestion~~
- ~~update-slash~~
- ~~init~~
- ~~message-command~~
- ~~reminder~~
- searchForXMLupdates
- thread-maker
- updateXML
- ~~index.js~~
- ~~deploy-commands.js -> guild commands for testing, global for deployment~~

## all
- confirm good commenting
- ~~confirm memory write updates happen before posts~~
- ~~implement memory.json read/write~~
- ~~implement bot.TESTING_MODE procedures~~
  - confirm it works and is consistent everywhere

## index.js
- ~~confirm everything matches up~~
- ~~implement status options~~

## ~~message-command.js~~ (deprecating)
- port all commands
- ~~get eval() to work ~~

## commands
- ~~social-media.js~~ (deferred for now)

## extras
- ~~Implement Modals~~ (ignored for now)
  - question submissions to Craig/GreenTeam
  - Suggestions to LRB
- implement bot.LOG_DEPTH for log clarity
 - a variable that gets larger the deeper into a functions logs it is
 - resets when function completes
 - wrap with try/catch blocks
- GT calendar? (requires GT support)
