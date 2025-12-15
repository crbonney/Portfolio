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
    .setName('status')
    .setDefaultMemberPermissions(PermissionFlagsBits.Administrator)
    .setDMPermission(false)
    // .addStringOption(new SlashCommandStringOption()
		// 	.setName('podcast_team')
		// 	.setDescription("Which podcast to look at series for?")
		// 	.addChoices({name: "Green Team", value: "greenTeam"})
		// 	.addChoices({name: "Main Team", value: "mainTeam"})
    //   .addChoices({name: "communityTest", value: "communityTest"})
		// 	.setRequired(false)
    // )
    .setDescription('Shows the stored episodes of the podcast teams in an embed.'),

  execute: async function(interaction,bot) {

    // read which series exist in memory
    const memory = readFileSync('./memory.json');
    // check which team they want to look at. if no options, display all
    // const teamName = interaction.options.getString('podcast_team');

    // store names of all teams to get series for in array
    const names = ['greenTeam','mainTeam']; // main use only has 2 teams
    if (TESTING_MODE) names.push('communityTest') // debug case includes test server

    const embed = new EmbedBuilder()
      .setTitle(`The episodes the bot currently has stored.`)
    ;

    // for each team, build an embed showing their active series and reply
    let first_reply = true;
    const fieldsObjArray = [];
    for (const name of names) {
      // build array of name/channel pairs for embed
      // for all series in "name"
      const episode = memory[name].latest_episode;
      fieldsObjArray.push({name: name,
        value:
`**Title:** ${episode.title}
**Link:** ${episode.link}
**Episode Number:** ${episode.number}
**Posting Next Episode:** ${memory[name].ignore_next.flag ? `No, notifying <@${memory[name].ignore_next.id}>` : "Yes"}
**Spotify ID:** ${episode.id}
**Description:** ${episode.description}
**Fake Episode Stored:** ${memory[name].fake ? "True" : "False"}
`
      });
    }

    embed.addFields(fieldsObjArray);
    await interaction.reply({embeds: [embed], ephemeral: true});

  }

}
