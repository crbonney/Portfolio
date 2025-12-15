
const { SlashCommandBuilder,
        SlashCommandStringOption,
        SlashCommandChannelOption,
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
    .setName('makeseries')
    .setDescription('Stores a new series of episodes for the bot to group together in one thread')
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
			.setDescription("The name of the series (should be a unique word/phrase in the title of all series episodes).")
			.setRequired(true)
		)
    .addChannelOption(new SlashCommandChannelOption()
			.setName('series_thread')
			.setDescription("If there already is a thread for this series, store that. Else, bot will create a thread for it.")
			.addChannelTypes(ChannelType.PublicThread)
			.setRequired(false)
		),


  async execute(interaction, bot) {

    // read which series already exist in memory
    const memory = readFileSync('./memory.json');

    // get the inputs of slash command
    const teamName = interaction.options.getString('podcast_team');
    const series_identifier = interaction.options.getString('series_name');
    // grab thread option (if given), and check if it already exists in memory
    let series_thread = interaction.options.getChannel('series_thread');


    const series_already_exists = memory[teamName].series.find(
      (series) => series.identifier == series_identifier
    );
    // if series already exists in memory, reply and return
    if (series_already_exists) {
      await interaction.reply({
        content: `Series for ${series_identifier} already exists in thread <#${series_already_exists.threadId}>. Use /activeseries for a full list of series stored by bot.`,
        ephemeral: true
      })
      return;
    }


    // if no series thread given, create a new one
    if (!series_thread) {
      series_thread = await bot.constants[teamName].forum.channel.threads.create({
        name: `${series_identifier}`,
        message: {content: `A thread for discussing the ${series_identifier} episodes`},
        appliedTags: [
          bot.constants[teamName].forum.channel.availableTags.find((tag) => {return tag.name == "Episode"}).id
        ]
      }).then((thread) => {series_thread_id = thread.id});
    } else {
      series_thread_id = series_thread.id;
      series_thread.edit({name: `${series_identifier} Episodes` })
    }

    // add new series to memory object and write it
    memory[teamName].series.push({
      "identifier": series_identifier,
      "threadId": series_thread_id
    });
    writeFileSync('./memory.json', memory, {spaces:2, EOL: '\r\n'});

    await interaction.reply({
      content: `Created Series for ${series_identifier}, with thread <#${series_thread_id}>`,
      ephemeral: true
    });

  }

}

// if in testing mode, include options for communityTest in podcast_team
if (TESTING_MODE) module.exports.data.options.find((o) => o.name === "podcast_team").choices.push({name: "communityTest", name_localizations: undefined, value: "communityTest"})
