
const { SlashCommandBuilder, SlashCommandStringOption, PermissionFlagsBits} = require('discord.js');
const {readFileSync, writeFileSync} = require('jsonfile'); //read/write memory JSON file
const {TESTING_MODE} = require('../bot-constants.json');
// ARUGMENTS:
// series identifier

// TASK
// remove object from "series" array of memory
// reply to interaction stating task complete

// TODO

module.exports = {

  data: new SlashCommandBuilder()
    .setName('endseries')
    .setDescription('Tells the bot to forget a series of episodes for it to stop grouping together in one thread')
    .setDefaultMemberPermissions(PermissionFlagsBits.Administrator)
    .setDMPermission(false)
    .addStringOption(new SlashCommandStringOption()
			.setName('podcast_team')
			.setDescription("Which podcast to update?")
			.addChoices({name: "Green Team", value: "greenTeam"})
			.addChoices({name: "Main Team", value: "mainTeam"})
			.setRequired(true)
		)
		.addStringOption(new SlashCommandStringOption()
			.setName('series_name')
			.setDescription("The name of the series to forget.")
			.setRequired(true)
		),


  async execute(interaction,bot) {

    // read which series already exist in memory
    const memory = readFileSync('./memory.json');

    // get the inputs of slash command
    const teamName = interaction.options.getString('podcast_team');
    const series_identifier = interaction.options.getString('series_name');

    filtered_memory = memory[teamName].series.filter((obj) => {
      return obj.identifier != series_identifier;
    });

    if (memory[teamName].series.length == filtered_memory.length) {
      console.log("Series was not found, no change made");
      await interaction.reply({
        content: `Could not find series ${series_identifier} in memory. Please check spelling and case sensitivity, or look at all series with /showseries.`,
        ephemeral: true
      });
      return
    }

    memory[teamName].series = filtered_memory;
    writeFileSync('./memory.json', memory, {spaces:2, EOL: '\r\n'});

    console.log(`Removed ${series_identifier} from list of series for ${teamName}.`)

    await interaction.reply({
      content: `Will no longer recognize ${series_identifier} as part of a series.`,
      ephemeral: true
    });
  }



}

// if in testing mode, include options for communityTest in podcast_team
if (TESTING_MODE) module.exports.data.options.find((o) => o.name === "podcast_team").choices.push({name: "communityTest", name_localizations: undefined, value: "communityTest"})
