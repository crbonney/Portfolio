
const { SlashCommandBuilder, SlashCommandStringOption, EmbedBuilder, PermissionFlagsBits} = require('discord.js');
const {readFileSync, writeFileSync} = require('jsonfile'); //read/write memory JSON file
const {TESTING_MODE} = require('../bot-constants.json');


// ARUGMENTS:
// none

// TASK
// get all objects from "series" array in memory
// reply to interaction with formatted list (embed?)


module.exports = {

  data: new SlashCommandBuilder()
    .setName('resetmemory')
    .setDefaultMemberPermissions(PermissionFlagsBits.Administrator)
    .setDMPermission(false)
    .addStringOption(new SlashCommandStringOption()
			.setName('podcast_team')
			.setDescription("Which podcast are you resetting the episode memory for?")
			.addChoices({name: "Green Team", value: "greenTeam"})
			.addChoices({name: "Main Team", value: "mainTeam"})
			.setRequired(true)
    )
    .setDescription('Resets the stored episode memory of the bot for testing purposes.'),

  execute: async function(interaction,bot) {

    // read which series exist in memory
    const memory = readFileSync('./memory.json');
    // check which team they want to look at. if no options, display all
    const teamName = interaction.options.getString('podcast_team');

    // remove the episode
    memory[teamName].latest_episode = {title: "reset", link: "abc.com", number: 0, id: "none", description: "none"};
    writeFileSync('./memory.json', memory, {spaces:2, EOL: '\r\n'});

    //
    await interaction.reply({
      content: `Reset the episode memory of ${teamName}.`, 
      ephemeral: true
    });
//    first_reply = false;


  }

}

// if in testing mode, include options for communityTest in podcast_team
if (TESTING_MODE) module.exports.data.options.find((o) => o.name === "podcast_team").choices.push({name: "communityTest", name_localizations: undefined, value: "communityTest"})
