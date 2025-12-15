const { SlashCommandBuilder, SlashCommandStringOption, PermissionFlagsBits } = require('discord.js');
const {TESTING_MODE} = require('../bot-constants.json');


module.exports = {
	data: new SlashCommandBuilder()
		.setName('spotify_update')
		.setDescription('Gets latest episode data from Spotify.')
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

		// await bot.functions.get('updateXML').execute(bot, interaction.options.getString('podcast_team'),
		// {ignoreNumberFlag: false, interaction: interaction});


		const data = await bot.functions.get('spotify-update').get_show_data(interaction.options.getString('podcast_team'));

		console.log(data);

		await interaction.reply({
			content: `Title: ${data.title}\n`
					+`URL: ${data.url}\n`
					+`ID: ${data.id}\n`
					+`Description: ${data.description}`
			,
			ephemeral: false
		});

	},
};

// if in testing mode, include options for communityTest in podcast_team
if (TESTING_MODE) module.exports.data.options.find((o) => o.name === "podcast_team").choices.push({name: "communityTest", name_localizations: undefined, value: "communityTest"})
