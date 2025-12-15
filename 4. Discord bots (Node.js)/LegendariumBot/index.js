
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// load in packages, and info/constants from JSON files
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Require the necessary discord.js classes
const {
  Client,
  Collection,
	Events,
	GatewayIntentBits,
	MessageEmbed,
	Permissions,
	Partials,
	ChannelType,
  ActionRowBuilder,
  ModalBuilder,
  TextInputBuilder,
  TextInputStyle,
  ActivityType
} = require('discord.js');

// fs and path for file reading
const fs = require('node:fs');
const path = require('node:path');
const {readFileSync, writeFileSync} = require('jsonfile');

// cron for monthly tasks
const Cron = require('cron').CronJob;

// read hidden token from config file
const { token } = require('./config.json');

// intents to give bot
const bot_requirements =
{
  partials:
  [
    Partials.Message,
    Partials.Channel,
    Partials.Reaction
  ],
  // create messages, channels and reactions
  // read messages, channels and reactions
  // in guild and direct messages
  intents:
  [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.GuildMessageReactions,
    GatewayIntentBits.GuildMembers,
    GatewayIntentBits.MessageContent,
    GatewayIntentBits.DirectMessages,
    GatewayIntentBits.DirectMessageReactions
  ]
};

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Create a new client instance with bot's requirements/intents
// preload constants and data to bot from json files
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
const bot = new Client(bot_requirements);

let memory;
// load in constants for the bot
bot.constants = require('./bot-constants.json');
// check if bot should load in testing mode or normal functionality
bot.TESTING_MODE = bot.constants.TESTING_MODE;

// load episode memory with readFile since we edit it, from jsonfile package
bot.memory = readFileSync('./memory.json');

// writeFileSync('./testfile.json', bot.memory, {spaces:2, EOL: '\r\n'})

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// create collections to hold bot's commands and functions, then grab those from their JS files
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// load constants from external file for cleanliness
// edit console.log to display time
console.logCopy = console.log.bind(console);

console.log = function (data) {
	var timestamp = `[${new Date().toLocaleString()}]`;
	this.logCopy(timestamp, data);
};


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// create collections to hold bot's commands and functions, then grab those from their JS files
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// create collections to store all the interaction commands and essential non-command functions of the bot
bot.commands = new Collection();
bot.functions = new Collection();

// get path to commands folder and add them to their respective collections
const commandsPath = path.join(__dirname, 'commands');
const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith('.js'));

// for each js file found in commands folder, check if it is a command and add to collection
for (const file of commandFiles) {
	const filePath = path.join(commandsPath, file);
	const command = require(filePath);
	// Set a new item in the Collection with the key as the command name and the value as the exported module
	if ('data' in command && 'execute' in command) {
    bot.commands.set(command.data.name, command);
	}
  else {
    // js files that did not have proper formatting for command or function
		console.log(`[WARNING] The command at ${filePath} is missing a required "data" or "execute" property.`);
	}
}

// get path to functions folder and add them to their respective collections
const functionsPath = path.join(__dirname, 'functions');
const functionsFiles = fs.readdirSync(functionsPath).filter(file => file.endsWith('.js'));

// for each js file found in functions folder, add to collection
for (const file of functionsFiles) {
	const filePath = path.join(functionsPath, file);
	const func = require(filePath);
	// Set a new item in the Collection with the key as the command name and the value as the exported module
    bot.functions.set(func.name, func);
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// variables and functions for CronJobs with end-of-month patreon submission reminders
// initialized on Events.ClientReady
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
let endofmonthalert;
let februaryalert;
const cron_func = async function() {
  console.log("Activating Cron Job");
  await bot.users.cache.get(bot.constants.users.rabbit.id).send("Reminder to submit Patreon Episodes. React with ❌ to delete this message.").then(msg => {
    msg.react(bot.constants.emojis.delete_dm_emoji);
  });
//  await bot.users.cache.get(bot.constants.users.lrb.id).send("Reminder to submit Patreon Episodes. React with ❌ to delete this message.").then(msg => {
//    msg.react(bot.constants.emojis.delete_dm_emoji);
//  });
//  await bot.users.cache.get(bot.constants.users.craig.id).send("Reminder to submit Patreon Episodes. React with ❌ to delete this message.").then(msg => {
//    msg.react(bot.constants.emojis.delete_dm_emoji);
//  });
}
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// When the bot client is ready, run this code (only once)
// client callback is bot
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
bot.once(Events.ClientReady, async client => {

  if (bot.TESTING_MODE) {
    // initialize test server only and set presence to clarify
    await bot.functions.get('init').community_test_data(bot);
    bot.user.setPresence({
      activities: [{type: ActivityType.Watching, name: "bugs in my code"}],
      status: 'dnd'
    });

  } else {
  // NOT IN TESTING MODE: ACTIVATE EVERYTHING
    await bot.functions.get('init').legendarium_data(bot);
    bot.user.setPresence({
      activities: [{type: ActivityType.Watching, name: "for new episodes"}],
      status: 'online'
    });

    // END OF MONTH PATREON SUBMISSION REMINDER ALERTS
    // on the 30th day of each month at noon, send LRB and Craig a reminder about Patreon Episodes
    endofmonthalert = new Cron('0 12 30 * *', cron_func, null, true, 'America/Los_Angeles');
    // on the February 28th at noon, send LRB and Craig a reminder about Patreon Episodes
    februaryalert = new Cron('0 12 28 2 *', cron_func, null, true, 'America/Los_Angeles');
  }

  // // inital automatic update on initialization
  // const gtxmlres = await bot.functions.get('updateXML').execute(bot,'greenTeam');
  // const xmlres = await bot.functions.get('updateXML').execute(bot,'mainTeam');

  // log ready after all initializing functions are complete
  console.log(`${client.user.tag} ready.`);

});

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// general console statements
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
bot.on("error", (err) => console.log(`ERROR: ${err}`));
bot.on("warn", (warn) => console.log(`WARN: ${warn}`));
// if (bot.TESTING_MODE) bot.on("debug", (debug) => console.log(`DEBUG: ${debug}`));

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// listener for Slash, ContextMenu and other Commands (buttons, modals, ect)
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
bot.on(Events.InteractionCreate, async interaction => {

  // // handle modal form submissions
  // if (interaction.isModalSubmit()) {
  //   interaction.reply({
  //     content: `Suggestion recieved! The mods will take a look when they get a chance. (Well right now it just goes to the void because I haven't implemented that part yet, but you get the idea)`,
  //     ephemeral: true
  //   });
  //   return;
  // }

  //handle button functions (UNUSED)
  if (interaction.isButton()) {
    // console.log(interaction.message.interaction);
    // interaction.reply(interaction.customId);
    // interaction.message.interaction.deleteReply();
    return;
  }

  // slash commands or context menu message commands
  if (interaction.isChatInputCommand() || interaction.isMessageContextMenuCommand()) {

    // check if command is in Collection. If not, log error and return
    const command = interaction.client.commands.get(interaction.commandName);
  	if (!command) return console.error(`No command matching ${interaction.commandName} was found.`);
    // if valid command, try executing
  	try {
  		await command.execute(interaction, bot);
  	} catch (error) {
      // if error in execution, log error and attempt to reply that there was an error
  		console.error(error);
  		await interaction.reply({ content: 'There was an error while executing this command!', ephemeral: true });
  	}
    return;
  }

});

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// listener for Messages
// sends welcome message to users who join the server
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
bot.on(Events.GuildMemberAdd, async (member) => {
  console.log(`${member.user.username} joined the server.`);
	if(member.guild == bot.constants.legendarium.server && !bot.TESTING_MODE) {
		await bot.constants.legendarium.general.channel.send(`Welcome, ${member}, to The Legendarium! Jump over to <#${bot.constants.legendarium.introductions.id}> and tell us a little about yourself and how you got into the podcast. And if you have one, declare your favorite panelist and we'll sort you into the proper ~~support group~~ house.`);
    return; 
	}
  if (member.guild == bot.constants.communityTest.server && bot.TESTING_MODE){
    await bot.constants.communityTest.forum_home.thread.send(`Weclome ${member.user}, to the test server.`);
    return;
  }
});

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// listener for Messages
// processes non-slash commands
// used only for episode management right now - requires role
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
bot.on(Events.MessageCreate, async (message) => {
  //if bot sent message, ignore
	if (message.author.equals(bot.user)) return;


	//if message doesn't start with prefix, ignore
	if (!message.content.startsWith(bot.constants.prefix)) return;

  // get user to determine if they have the proper roles
  // uses specified server instead of message.guild to work in DMs
  const user = (bot.TESTING_MODE)
    ? bot.constants.communityTest.server.members.cache.get(message.author.id)
    : bot.constants.legendarium.server.members.cache.get(message.author.id)
  ;


  // compares the users roles to the list of role IDs allowed to manage episodes
	const user_has_episode_management_role = await user.roles.cache
    .some( (role) => bot.constants.episode_management_roles.find((obj) => obj.name === role.name));
  // if no permission, return
  if (!user_has_episode_management_role) return console.log(`${message.author.username} tried to manage episodes without permissions.`);

	//checks what command to run and runs it
  try {
    await bot.functions.get('message command').process_command(message, bot);
  } catch (error) {
    console.error(error);
    await message.reply(`there was an error executing command`);
    await bot.users.cache.get(bot.constants.rabbit.id).send(`error executing message command: ${error}`);
  }

});

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// listener for Reactions
// for reaction roles and reaction reminders
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
bot.on(Events.MessageReactionAdd,  async (reaction,user) => {
  //checks if the reaction is partial (incomplete data)
  if (reaction.partial) {
      // if it is, try awaiting its data
      try {
          await reaction.fetch(); //fetches reaction because not every reaction is stored in the cache
      } catch (error) {
          console.error('Fetching message failed: ', error); //fetching data failed, log error
          return;
      }
  }

  if (user.bot) return; // dont respond to bots reacting

  // if message is a DM, and the reaction is the emoji to delete messages, delete that message
  if (reaction.message.channel.type === ChannelType.DM && reaction.message.author.equals(bot.user) && reaction._emoji.name == bot.constants.emojis.delete_dm_emoji) {
		reaction.message.delete();
    console.log(`deleting reminder for ${user.username}`);
    return;
	}

  // send reaction reminder
  if (reaction._emoji.name === bot.constants.emojis.reminder_emoji) {
    bot.functions.get('reminder').reminder(reaction.message,user);
    return;
  }

  // reaction role add/remove
  if (reaction.message.id == bot.constants.legendarium.react_roles.id) {
    // look for role/emoji pair in database
    const role_to_assign = bot.constants.react_role_data.find(role => role.emoji === reaction._emoji.name);

    if (!role_to_assign) return; // did not find a role emoji, return

    // get reacting user and their desired role, then add role
    const server_role = bot.constants.legendarium.server.roles.cache.get(role_to_assign.id);
    const server_user = bot.constants.legendarium.server.members.cache.find(member => member.id === user.id);

    server_user.roles.add(server_role);
    console.log(`Added role ${role_to_assign.name} to user ${user.username} with reaction`);
    return;
  }
});

bot.on(Events.MessageReactionRemove,  async (reaction,user) => {
  //checks if the reaction is partial (incomplete data)
  if (reaction.partial) {
      // if it is, try awaiting its data
      try {
          await reaction.fetch(); //fetches reaction because not every reaction is stored in the cache
      } catch (error) {
          console.error('Fetching message failed: ', error); //fetching data failed, log error
          return;
      }
  }

  if (user.bot) return; // dont respond to bots reacting

  // reaction role add/remove
  if (reaction.message.id == bot.constants.legendarium.react_roles.id) {
    // look for role/emoji pair in database
    const role_to_assign = bot.constants.react_role_data.find(role => role.emoji === reaction._emoji.name);

    if (!role_to_assign) return; // did not find a role emoji, return

    // get reacting user and their desired role, then remove role
    const server_role = bot.constants.legendarium.server.roles.cache.get(role_to_assign.id);
    const server_user = bot.constants.legendarium.server.members.cache.find(member => member.id === user.id);

    server_user.roles.remove(server_role);
    console.log(`Removed role ${role_to_assign.name} to user ${user.username} with reaction`);
    return;
  }
});



// Log in to Discord with your client's token
bot.login(token);
