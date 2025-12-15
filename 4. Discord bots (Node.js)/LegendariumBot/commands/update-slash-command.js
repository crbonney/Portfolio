const { SlashCommandBuilder, SlashCommandStringOption, PermissionFlagsBits } = require('discord.js');
const {TESTING_MODE} = require('../bot-constants.json');
const spotify_updates = require('../functions/spotify-update.js');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('update')
		.setDescription('Manually updates XML of a podcast.')
		.setDefaultMemberPermissions(PermissionFlagsBits.Administrator)
		.setDMPermission(false)
		.addStringOption(new SlashCommandStringOption()
			.setName('podcast_team')
			.setDescription("Which podcast to update?")
			.addChoices({name: "Green Team", value: "greenTeam"})
			.addChoices({name: "Main Team", value: "mainTeam"})
			.setRequired(true)
		),
	async execute(interaction,bot) {
		// interaction.user is the object representing the User who ran the command
		// interaction.member is the GuildMember object, which represents the user in the specific guild

		console.log(`manual update called by ${interaction.user.username}`);

		// runs updateXML function with optional args for interaction data
		await bot.functions.get('updateXML').execute(bot, interaction.options.getString('podcast_team'),
		{ignoreNumberFlag: false, interaction: interaction});


	},
};

// if in testing mode, include options for communityTest in podcast_team
if (TESTING_MODE) module.exports.data.options.find((o) => o.name === "podcast_team").choices.push({name: "communityTest", name_localizations: undefined, value: "communityTest"})
