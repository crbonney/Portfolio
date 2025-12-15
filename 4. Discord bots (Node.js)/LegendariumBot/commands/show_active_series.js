
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
    .setName('showactiveseries')
    .setDefaultMemberPermissions(PermissionFlagsBits.Administrator)
    .setDMPermission(false)
    .addStringOption(new SlashCommandStringOption()
			.setName('podcast_team')
			.setDescription("Which podcast to look at series for?")
			.addChoices({name: "Green Team", value: "greenTeam"})
			.addChoices({name: "Main Team", value: "mainTeam"})
			.setRequired(false)
    )
    .setDescription('Shows the active series of the podcast in an embed.'),

  execute: async function(interaction,bot) {

    // read which series exist in memory
    const memory = readFileSync('./memory.json');
    // check which team they want to look at. if no options, display all
    const teamName = interaction.options.getString('podcast_team');

    // store names of all teams to get series for in array
    let names;
    if (!teamName) {
      names = ['greenTeam','mainTeam']; // main use only has 2 teams
      if (TESTING_MODE) names.push('communityTest') // debug case includes test server
    } else {
      names = [teamName];
    }

    // for each team, build an embed showing their active series and reply
    let first_reply = true;
    for (const name of names) {
      // build array of name/channel pairs for embed
      const fieldsObjArray = [];
      // for all series in "name"
      for (const series of memory[name].series) {
        // {name: "identifier", value: <#channeL>}
        fieldsObjArray.push({name: series.identifier,
        value: `<#${series.threadId}>`});
      }

      const embed = new EmbedBuilder()
        .setTitle(`Active Series for ${name}`)
        .addFields(fieldsObjArray)
      ;

      if (first_reply) {
        await interaction.reply({embeds: [embed], ephemeral: true});
        first_reply = false;
      } else {
        // .reply is only for first reply, all others are .followup
        await interaction.followUp({embeds: [embed], ephemeral: true});
      }
    }

  }

}

// if in testing mode, include options for communityTest in podcast_team
if (TESTING_MODE) module.exports.data.options.find((o) => o.name === "podcast_team").choices.push({name: "communityTest", name_localizations: undefined, value: "communityTest"})
