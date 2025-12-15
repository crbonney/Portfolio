
const { SlashCommandBuilder, SlashCommandStringOption} = require('discord.js');

const legendarium_website_url = "https://www.thelegendarium.com/";
module.exports = {

  data: new SlashCommandBuilder()
    .setName('episodecalendar')
    .setDescription('Sends the user a link to legendarium website where the calendar is hosted.')
    .setDMPermission(true)
    // .addStringOption(new SlashCommandStringOption()
		// 	.setName('podcast_team')
		// 	.setDescription("Which podcast to update?")
		// 	.addChoices({name: "Green Team", value: "greenTeam"})
		// 	.addChoices({name: "Main Team", value: "mainTeam"})
		// 	.setRequired(true)
		// )
    ,

  async execute(interaction, bot) {
    await interaction.reply({
      content: `The calendar is available at ${legendarium_website_url}`,
      ephemeral: true
    });

  }
}
