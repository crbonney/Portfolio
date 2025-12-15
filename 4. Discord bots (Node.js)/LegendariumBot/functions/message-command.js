const {readFileSync, writeFileSync} = require('jsonfile'); //read/write memory JSON file

module.exports = {

  name: "message command",
  description: "takes in a message with correct prefix and finds/preforms the correct command",


  process_command: async function(message, bot) {

    console.log(`executing "${message.content}" from ${message.author.username}`);
    //filters arguments for the command from the message, by setting to lower case, spliting into substrings, and removing any leftover blanks
    let args = message.content.substring(bot.constants.prefix.length).toLowerCase().split(" ").filter(arg => arg != '');

    // message.content = !args[0] args[1] args[2] ...
    switch (args[0]) {
      case "ping": return await message.reply("pong");

      // // manually updates mainTeam XML, and repeats every minute until it either finds it or 30 minutes pass
      // case "update":
      //   console.log("| manual update called");
      //   await bot.functions.get('updateXML').execute(bot, "mainTeam", {interaction: message});
      //   await message.react(bot.constants.emojis.confirm_emoji);
      // return;

      // // manually updates greenTeam XML
      // case "updategt":
      //   console.log("| gt manual update called");
      //   await bot.functions.get('updateXML').execute(bot, "greenTeam", {interaction: message});
      //   await message.react(bot.constants.emojis.confirm_emoji);
      // return;

      // case "ignore":
      //   // update bot memory
      //   bot.memory = readFileSync('./memory.json');
      //
      // return;
      //
      // case "ignoregt":
      //   // update bot memory
      //   bot.memory = readFileSync('./memory.json');
      //
      // return;

      // case "status":
      //   // update bot memory
      //   bot.commands.get('status').execute(message, bot);
      //   bot.memory = readFileSync('./memory.json');
      //
      // return;

      // case "manualpost":
      //   // update bot memory
      //   bot.memory = readFileSync('./memory.json');
      //
      // return;


      // case "manualpostgt":
      //   // update bot memory
      //   bot.memory = readFileSync('./memory.json');
      //
      // return;
    }


  }

}
