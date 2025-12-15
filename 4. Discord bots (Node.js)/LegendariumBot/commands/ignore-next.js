const {
  SlashCommandBuilder,
  SlashCommandStringOption,
  SlashCommandBooleanOption,
  EmbedBuilder,
  PermissionFlagsBits
} = require('discord.js');
const {readFileSync, writeFileSync} = require('jsonfile'); //read/write memory JSON file
const {TESTING_MODE} = require('../bot-constants.json');


// ARUGMENTS:
// Team Name 
// Boolean flag

// TASK
// read the team name and flag
// write into the "ignore-next" flag option for that team in memory

module.exports = {

  data: new SlashCommandBuilder()
    .setName('ignorenext')
    .setDefaultMemberPermissions(PermissionFlagsBits.Administrator)
    .setDMPermission(false)
    .addStringOption(new SlashCommandStringOption()
			.setName('podcast_team')
			.setDescription("Which podcast are you setting the flag for?")
			.addChoices({name: "Green Team", value: "greenTeam"})
			.addChoices({name: "Main Team", value: "mainTeam"})
			.setRequired(true)
    )
    .addBooleanOption(new SlashCommandBooleanOption()
			.setName('flag_boolean')
			.setDescription("Are you turning the flag on or off?")
			// .addChoices({name: "On", value: true})
			// .addChoices({name: "Off", value: false})
			.setRequired(true)
    )
    .setDescription('Turns on/off the "ignore next flag" for a podcast.'),

  execute: async function(interaction,bot) {

    // read which series exist in memory
    const memory = readFileSync('./memory.json');
    // check which team they want to look at. if no options, display all
    const teamName = interaction.options.getString('podcast_team');
    const flag_boolean = interaction.options.getBoolean('flag_boolean');

    memory[teamName].ignore_next.flag = flag_boolean;
    memory[teamName].ignore_next.id = interaction.user.id;
    writeFileSync('./memory.json', memory, {spaces:2, EOL: '\r\n'})
    console.log("memory updated with ignoreNext flag");

    interaction.reply({
      content:
        `I will now ${flag_boolean ? "ignore" : "post"}`
        +` the next episode for ${teamName}`
        +`${flag_boolean ? `, and notify ${interaction.user} when I've found one` : ""}.`
      ,
      ephemeral: true
    });

  }

}


// if in testing mode, include options for communityTest in podcast_team
if (TESTING_MODE) module.exports.data.options.find((o) => o.name === "podcast_team").choices.push({name: "communityTest", name_localizations: undefined, value: "communityTest"})
