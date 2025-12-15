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
// write into the "thread-next" flag option for that team in memory

module.exports = {

  data: new SlashCommandBuilder()
    .setName('thread-next')
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
			.setDescription("Would you like the next episode to be posted in a new thread?")
			// .addChoices({name: "On", value: true})
			// .addChoices({name: "Off", value: false})
			.setRequired(true)
    )
    .setDescription('Turns on/off the "new thread flag" for a podcast. [not working yet]'),

  execute: async function(interaction,bot) {

    // read in memory
    const memory = readFileSync('./memory.json');

    // get team and flag boolean from command
    const teamName = interaction.options.getString('podcast_team');
    const flag_boolean = interaction.options.getBoolean('flag_boolean');

    // write flag into memory
    memory[teamName].thread_next.flag = flag_boolean;
    writeFileSync('./memory.json', memory, {spaces:2, EOL: '\r\n'})
    console.log("memory updated with ignoreNext flag");

    // notify result
    interaction.reply({
      content:
        `I will now post the next episode for` 
      + `${teamName} ${flag_boolean ? "in a new thread" : "as normal"}.`
      ,
      ephemeral: true
    });
  }
}


// if in testing mode, include options for communityTest in podcast_team
if (TESTING_MODE) module.exports.data.options.find((o) => o.name === "podcast_team").choices.push({name: "communityTest", name_localizations: undefined, value: "communityTest"})
