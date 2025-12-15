const { REST, Routes } = require('discord.js');
const {token} = require('./config.json');
const fs = require('node:fs');

const bot_info = require('./bot-constants.json');
const clientId = bot_info.users.bot.id;
const guildId = bot_info.communityTest.id;

const commands = [];
// Grab all the command files from the commands directory you created earlier
const commandFiles = fs.readdirSync('./commands').filter(file => file.endsWith('.js'));

// Grab the SlashCommandBuilder#toJSON() output of each command's data for deployment
for (const file of commandFiles) {
	const command = require(`./commands/${file}`);

  // only look for js files that have data, execute, and are commands (not functions)
  if ('data' in command && 'execute' in command && command.data.type != 'function') {
	  commands.push(command.data.toJSON());
		console.log(command.data.name);
   }
}

// Construct and prepare an instance of the REST module
const rest = new REST({ version: '10' }).setToken(token);

// and deploy your commands!
(async () => {
	try {
		console.log(`Started refreshing ${commands.length} application (/) commands.`);

		// // The put method is used to fully refresh all commands in the guild with the current set
		// // best used for testing new commands
		// const guild_data = await rest.put(
		// 	Routes.applicationGuildCommands(clientId, guildId),
		// 	{ body: commands },
		// );
		// console.log(`Successfully reloaded ${guild_data.length} application (/) commands to guild.`);

		// The put method is used to fully refresh all commands everywhere with the current set
		const global_data = await rest.put(
			Routes.applicationCommands(clientId),
			{ body: commands },
		);
		console.log(`Successfully reloaded ${global_data.length} application (/) commands globally.`);

	} catch (error) {
		// And of course, make sure you catch and log any errors!
		console.error(error);
	}
})();
