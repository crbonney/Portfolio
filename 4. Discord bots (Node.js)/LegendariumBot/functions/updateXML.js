
// const searchForXMLupdates = require('./searchForXMLupdates.js');
const spotify_updates = require('./spotify-update.js');
const {readFileSync, writeFileSync} = require('jsonfile'); //read/write memory JSON file
const {ActionRowBuilder, ButtonBuilder, ButtonStyle} = require('discord.js');
const wait = require('node:timers/promises').setTimeout;

// default options for
const defaultOptions = {
  ignoreNumberFlag: false, //ignore warning flags (like new episode# being smaller than stored episode#) and post episode anyways
  // interaction: , //command that called the function. defaults to undefined for automatic updates
  // makeSeries: { //if the episode is the start of a series (or just initializing the existing series for the bot)
  //   identifier: "a string that all episodes in this series will contain",
  //   threadId: "id of thread for series if it has already been made (optional)",
  //   ignoreDetectedSeries: false //creates new series even if it was detected to be in series already
  // }
};


module.exports = {
  name: "updateXML",
  description: "runs spotify-update, and determines if it should post episode or process flag",

  async execute(bot, teamName, options=defaultOptions) {

    // read in most recent copy of memory
    const memory = readFileSync('./memory.json');

    // get and parse episode data from XML
    // let newEpisodeData = await searchForXMLupdates.execute(teamName);
    let newEpisodeData = await spotify_updates.get_show_data(teamName);


    // if an automatic update has no result, return
    if ((newEpisodeData.episode.id == memory[teamName].latest_episode.id)  && !options.interaction) {
      console.log("| no new episode on automatic update, returning");
      return
    }

    // if !options.interaction -> then an automatic update found a new episode
    // update memory, post it and return
    if (!options.interaction) {

      // if fake episode is found by auto update, turn off the fake and return
      if (memory[teamName].fake) {
        console.log("Automatic update found Fake episode, not posting.");
        memory[teamName].fake = false;
        writeFileSync('./memory.json', memory, {spaces:2, EOL: '\r\n'})
        return;
      }

      // ignore_next flag triggered by auto update
      // alert user who triggered the flag, update memory and return
      if (memory[teamName].ignore_next.flag || newEpisodeData.flag) {
        console.log(`| found new episode, but it had a flag, updating memory, notifying and returning.`);

        // start construct warning message to send to user
        let flag_warning = `A new episode was found, **${newEpisodeData.episode.title}**, but there was a flag: `;
        
        // add appropriate message to warning based on flag
        if (memory[teamName].ignore_next.flag) {
          flag_warning += "ignore next episode was requested.";
          // turn off ignore next flag
          memory[teamName].ignore_next.flag = false;
        } else if (newEpisodeData.flag == "ID_FLAG") {
          flag_warning += "the Spotify ID matches the previous episode."
//        } else if (newEpisodeData.flag == "NUMBER_FLAG") {
//          flag_warning += "the episode's number was lower/equal to the one I have stored."
        } else { // flag showed up but didnt match any known flags
          flag_warning += "Unknown error."
        }

        flag_warning += "\nI did not post the episode in case of an error. If you would like to post it, use \`/manualpost\`. Otherwise, do nothing."

        // update and save memory
        memory[teamName].latest_episode = newEpisodeData.episode;
        writeFileSync('./memory.json', memory, {spaces:2, EOL: '\r\n'});

        // notify and return

        // always notify me
        await bot.users.cache.get(bot.constants.rabbit.id).send(flag_warning);
        // if im not in the memory as the notifyee, notify that person as well
        if (memory[teamName].ignore_next.id != bot.constants.rabbit.id) {
          await bot.users.cache.get(memory[teamName].ignore_next.id).send(flag_warning);
        }
        return;

      }

      // No flag was found on new auto update episode found - update memory and post

      console.log("| found new episode, updating memory");
      memory[teamName].latest_episode = newEpisodeData.episode;
      writeFileSync('./memory.json', memory, {spaces:2, EOL: '\r\n'})

      await bot.functions.get('post-episode').post(teamName,newEpisodeData,bot);
      return

    }

    // must be an interaction, reply to it
    const interactionReply = await options.interaction.reply({
      content: "searching...",
      components: [],
      ephemeral: true,
      fetchReply: true
    });

    // if there is no new episode on interaction:
    // notify and keep searching.
    // if episode if found in time, continue, otherwise return
    if (newEpisodeData.episode.id == memory[teamName].latest_episode.id) {
      console.log("| no new episode, notifying and continuing search.");

      // keep searching for episodes for 10 minutes
      for (let counter = 0; counter < 10; counter++) {
        await options.interaction.editReply(`no new episode found yet, I will keep searching every 60 seconds and notify you if I find anything (${10-counter} attempts remaining). Do not dismiss this message yet.
current stored episode is **${newEpisodeData.episode.title}**.`);

        // wait 1 minute for next search
        await wait(1000*60 / (bot.TESTING_MODE ? 10 : 1)); // shorten time for testing mode
        console.log(`| search counter: ${counter}`);

        // search again
        newEpisodeData = await spotify_updates.get_show_data(teamName);
        // newEpisodeData.ID_FLAG is triggered if the episode is the same
        if(!newEpisodeData.flag || newEpisodeData.flag != "ID_FLAG") break //exit loop if episode is found
      }

      // if didnt find new episode in time, notify and return
      if (!newEpisodeData.episode == true) {
        console.log("| Did not find any episodes, stopping search.");
        await options.interaction.editReply(`Did not find any episodes, stopping search (you may dismiss this message).`);
        return
      }

      // found new episode, ping interactor to notify them
      console.log("| found episode.");
      await options.interaction.editReply(`Found new episode.`);
      await options.interaction.followUp({
        content: `${options.interaction.user}, I found a new episode, (this message is just to tag you, you can dismiss it).`,
        ephemeral: true
      });
    }

    ////////////////////////////////////////////////////////////////////////////////
    // if here, then a new episode was found, and is an interaction
    ////////////////////////////////////////////////////////////////////////////////

    // store temp memory to use later so we can make sure we
    // update memory before posting, so errors wont cause double post
    const temp_memory = {};
    temp_memory.previous_episode = memory[teamName].latest_episode;
    temp_memory.ignore_next = memory[teamName].ignore_next.flag;

    // update memory
    memory[teamName].latest_episode = newEpisodeData.episode;
    memory[teamName].ignore_next.flag = false;
    writeFileSync('./memory.json', memory, {spaces:2, EOL: '\r\n'})
    console.log("| memory updated with new episode");

    // post choices to post/not post to interaction user with buttons
    const row = new ActionRowBuilder()
    .addComponents(
      new ButtonBuilder()
      .setCustomId('yes')
      .setLabel('Yes')
      .setStyle(ButtonStyle.Primary),
    )
    .addComponents(
      new ButtonBuilder()
      .setCustomId('no')
      .setLabel('No')
      .setStyle(ButtonStyle.Danger),
    );

    // send button response
    await options.interaction.editReply({
      content:
        `New episode found: ${newEpisodeData.episode.title}`
        + `${newEpisodeData.series ? `\nIn series <#${newEpisodeData.series.threadId}>.` : "."}`
        + `\nshall I post it?`
        + `${newEpisodeData.flag ? `\n**WARNING:** This episode was flagged for having a lower/equal number to the prior stored episode (${temp_memory.previous_episode.title}).` : ""}`
        + `${temp_memory.ignore_next ? `\n**WARNING:** I had a flag to ignore the next epsiode found (the flag has been reset to off). Double check you want to post this.` : ""}`
      ,
      components: [row],
      ephemeral: true,
      fetchReply: true
    });

    // read button press from user for 15 minutes
    const filter = (i) => i.user.id == options.interaction.user.id;
    const collector = options.interaction.channel.createMessageComponentCollector({ filter, time: bot.constants.HOUR/4, max: 1});
    collector.on('collect', async i => {
      // if a fake episode exists, resolve that now
      if (memory[teamName].fake) {
        memory[teamName].fake = false;
        writeFileSync('./memory.json', memory, {spaces:2, EOL: '\r\n'});
      }

      // if "Yes" was pressed, post episode
      if (i.customId == 'yes') {
        await options.interaction.editReply({
          content: `Attempting to post Episode`,
          components: []
        });
        await bot.functions.get('post-episode').post(teamName,newEpisodeData,bot);

      } else {
        console.log("| episode post option was declined.");
        await options.interaction.editReply({
          content: `Not posting new episode. If you would like to post it manually later, or post it not in the identified series, use \`/postepisode\``,
          components: []
        });
      }
    });

    // at end of 60 seconds (when maxed at 1 press)
    collector.on('end', async (collected) => {
      // if collected anything, button was already removed
      if(collected.size > 0) return;

      // otherwise user didn't press button, notify and give options
      console.log("| user did not respond to button in time.");
      await options.interaction.editReply({
        content: `Did not recieve reply. If you would like to post it manually later, or post it not in the identified series, use \`/postepisode\``,
        components: []
      });

    });


    return;
  }


}
