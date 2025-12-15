
const { SlashCommandBuilder,
        SlashCommandStringOption,
        ChannelType,
        PermissionFlagsBits
} = require('discord.js');
const {readFileSync, writeFileSync} = require('jsonfile'); //read/write memory JSON file
const {TESTING_MODE} = require('../bot-constants.json');

// ARUGMENTS:
// series identifier
// [optional] thread of already active series

// TASK
// if [optional] thread :
// -> edit thread title and descriptoin to match new identifier
// else :
// -> create thread for series
// store identifier and thread as object in "series" array of memory
// reply to interaction stating task complete

module.exports = {

  data: new SlashCommandBuilder()
    .setName('fakeepisode')
    .setDescription('For testing: makes the bot find a fake episode on its next update')
    .setDefaultMemberPermissions(PermissionFlagsBits.Administrator)
    .setDMPermission(false)
    .addStringOption(new SlashCommandStringOption()
			.setName('podcast_team')
			.setDescription("Which podcast to post an episode for?")
			.addChoices({name: "Green Team", value: "greenTeam"})
			.addChoices({name: "Main Team", value: "mainTeam"})
			.setRequired(true)
		)
		.addStringOption(new SlashCommandStringOption()
			.setName('episode_name')
			.setDescription("The title of the fake episode to find (include a number in that, #123).")
			.setRequired(true)
		)
    .addStringOption(new SlashCommandStringOption()
			.setName('episode_link')
			.setDescription("A link for the fake episode (if not given, will default to 'abc.com').")
			.setRequired(false)
		)
    .addStringOption(new SlashCommandStringOption()
      .setName('episode_description')
      .setDescription("A description for the episode (if not given, will default to none).")
      .setRequired(false)
    ),

  async execute(interaction, bot) {

    // if the bot isn't in testing mode, do not process command
    if (!bot.TESTING_MODE) {
      console.error("attempted to make a fake episode while not in testing mode.");
      return await interaction.reply({
        content: `The bot is not in Test Mode, so this command was not processed.`,
        ephemeral: true
      });
    }

    // read which series already exist in memory
    const memory = readFileSync('./memory.json');

    // get the inputs of slash command
    const teamName = interaction.options.getString('podcast_team');
    const episode_name = interaction.options.getString('episode_name');
    // grab thread option (if given), and check if it already exists in memory
    const episode_link = interaction.options.getString('episode_link') ?? "abc.com";
    const episode_description = interaction.options.getString('episode_link') ?? "";


    // add fake episode to memory and write
    memory[teamName].fake = {
      title: episode_name,
      link: episode_link,
      description: episode_description
    };
    writeFileSync('./memory.json', memory, {spaces:2, EOL: '\r\n'});


    console.log(`Creating a fake episode to be found`)

    await interaction.reply({
      content: `The bot will now find ${episode_name}, when it next searches for a ${teamName} episode. You can trigger this with \`/update\`.`,
      ephemeral: true
    });

  }

}

// if in testing mode, include options for communityTest in podcast_team
if (TESTING_MODE) module.exports.data.options.find((o) => o.name === "podcast_team").choices.push({name: "communityTest", name_localizations: undefined, value: "communityTest"})
