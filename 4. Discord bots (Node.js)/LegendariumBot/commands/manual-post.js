const {
  SlashCommandBuilder,
  SlashCommandStringOption,
  SlashCommandChannelOption,
  ChannelType,
  EmbedBuilder,
  PermissionFlagsBits,
  ActionRowBuilder,
  ButtonBuilder,
  ButtonStyle
} = require('discord.js');
const {readFileSync, writeFileSync} = require('jsonfile'); //read/write memory JSON file
const {TESTING_MODE} = require('../bot-constants.json');


// ARUGMENTS:
// none

// TASK
// get all objects from "series" array in memory
// reply to interaction with formatted list (embed?)


module.exports = {

  data: new SlashCommandBuilder()
    .setName('postepisode')
    .setDefaultMemberPermissions(PermissionFlagsBits.Administrator)
    .setDMPermission(false)
    .addStringOption(new SlashCommandStringOption()
			.setName('podcast_team')
			.setDescription("Which podcast are you setting the flag for?")
			.addChoices({name: "Green Team", value: "greenTeam"})
			.addChoices({name: "Main Team", value: "mainTeam"})
			.setRequired(true)
    )
    .addStringOption(new SlashCommandStringOption()
    .setName('send_alert')
    .setDescription("Do you want an @alert for this post? (*default will alert*)")
			.addChoices({name: "Yes", value: "true"})
			.addChoices({name: "No", value: "false"})
			.setRequired(false)
    )
    .addStringOption(new SlashCommandStringOption()
			.setName('post_series')
			.setDescription("Do you want to post this episode as part of a series? (default: yes if a series has been identified)")
      .addChoices({name: "Yes", value: "true"})
			.addChoices({name: "No", value: "false"})
			.setRequired(false)
    )
    .addChannelOption(new SlashCommandChannelOption()
      .setName('series_thread')
      .setDescription("If there is a specific thread you want to post this episode in, put it here.")
      .addChannelTypes(ChannelType.PublicThread)
      .setRequired(false)
    )
    .setDescription('Manually posts the thread for a new episode, with options for alert/series.'),

  execute: async function(interaction,bot) {

    // check which team they want to look at. if no options, display all
    const teamName = interaction.options.getString('podcast_team');
    let send_alert = interaction.options.getString('send_alert') ?? "true";
    send_alert = send_alert == "true" ? true : false;
    let post_series = interaction.options.getString('post_series') ?? "true";
    post_series = post_series == "true" ? true : false;

    // read in memory for team
    const teamMemory = readFileSync('./memory.json')[teamName];

    console.log(`manual posting episode for ${teamName} with send_alert: ${send_alert}, post_series: ${post_series}`);

    // post choices to post/not post to interaction user with buttons
    const row = new ActionRowBuilder()
    .addComponents(
      new ButtonBuilder()
      .setCustomId('yes')
      .setLabel('Post')
      .setStyle(ButtonStyle.Primary),
    )
    .addComponents(
      new ButtonBuilder()
      .setCustomId('no')
      .setLabel("Don't post")
      .setStyle(ButtonStyle.Danger),
    );

    // check if episode belongs in series, if match found, add information to resultObject
    for (const series of teamMemory.series) {
      const identifier_regex = new RegExp(series.identifier);
      // console.log(identifier_regex);
      const series_match = teamMemory.latest_episode.title.match(identifier_regex);
      // console.log(series_match);
      if (series_match) {
        teamMemory.latest_episode.series = series;
        console.log(`| found episode to be in ${series.identifier}`);
        break;
      }
    }

    // if a series series_thread was provided in options, overwrite series info to that
    if (interaction.options.getChannel('series_thread')) {
        teamMemory.latest_episode.series = {};
        teamMemory.latest_episode.series.identifier = "override";
        teamMemory.latest_episode.series.threadId = interaction.options.getChannel('series_thread').id;
    }



    const episode_data = {
      episode: teamMemory.latest_episode,
      teamName: teamName,
      series: teamMemory.latest_episode.series
    }
    console.log(`| episode series info: ${episode_data.series}`);

    // send button response
    await interaction.reply({
      content:
        `Do you want me to post episode *${teamMemory.latest_episode.title}*`
        + `${(episode_data.series && post_series) ? `, in series thread <#${episode_data.series.threadId}>` : " in a new thread"}`
        + `${(send_alert) ? `, with an alert?` : ", without an alert?"}`
        + `${(episode_data.series && !post_series) ? `\n**WARNING:** this episode was flagged to be in <#${episode_data.series.threadId}>, but I've been told to not post it there. Is that right?` : ""}`
      ,
      components: [row],
      ephemeral: true,
      fetchReply: true
    });


    // read button press from user for 15 minutes
    const filter = (i) => i.user.id == interaction.user.id;
    const collector = interaction.channel.createMessageComponentCollector({ filter, time: bot.constants.HOUR/4, max: 1});
    collector.on('collect', async i => {
      // if "Yes" was pressed, post episode
      if (i.customId == 'yes') {
        await interaction.editReply({
          content: `Posting Episode`,
          components: []
        });
        console.log("| attempting to post episode...");
        await bot.functions.get('post-episode').post(teamName,episode_data,bot,{alert: send_alert, series: post_series});
      } else {
        console.log("| episode post option was declined.");
        await interaction.editReply({
          content: `Not posting new episode. If you would like to post it manually later, or post it not in the identified series, use \`/postepisode\``,
          components: []
        });
      }
    });


  }

}


// if in testing mode, include options for communityTest in podcast_team
if (TESTING_MODE) module.exports.data.options.find((o) => o.name === "podcast_team").choices.push({name: "communityTest", name_localizations: undefined, value: "communityTest"})
