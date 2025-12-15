
const defaultOptions = {
  alert: true,
  series: true
}

module.exports = {

  name: "post-episode",
  description: "Creates a thread for an episode (or gets the current one if a series), posts it there and alerts",

  post: async function (teamName, newEpisodeData, bot, options=defaultOptions) {

    // // requested a new thread for next episode
    // if (memory[teamName].thread_next.flag) {
    //   console.log(`| post options: new thread`);
      
    // }


// console.log(bot.constants[teamName].forum_home.thread)
    console.log(`| post options: ${JSON.stringify(options)}`);
    // if episode is in a series, get the thread for the series, post it there, then alert in home
    if (newEpisodeData.series && options.series) {
      console.log("| posting series episode.");
      const thread = await bot.constants[teamName].forum.channel.threads.fetch(newEpisodeData.series.threadId);
      await thread.send(`NEW Episode: **${newEpisodeData.episode.title}** `
        + "\n" + newEpisodeData.episode.description
        + "\n" + newEpisodeData.episode.link);
      await bot.constants[teamName].forum_home.thread.send(
        `${options.alert ? `<@&${bot.constants[teamName].alert_role.id}> ` : ""} new episode for`
        + ` ${thread}: ${newEpisodeData.episode.title}`
      );
      return;
    }

    // otherwise, make a non-thread for the episode in home and alert
    console.log("| posting non-series episode in main thread.");
    // // make channel thread (not using this anymore)
    // bot.constants[teamName].forum.channel.threads.create({
    //   name: `${newEpisodeData.episode.title}`,
    //   message: {content: `${newEpisodeData.episode.description}`},
    //   appliedTags: [
    //     bot.constants[teamName].forum.channel.availableTags.find((o) => {return o.name == "Episode"}).id
    //   ]
    // }).then((chnl) => {
    //   bot.constants[teamName].forum_home.thread.send(
    //     `${options.alert ? `<@&${bot.constants[teamName].alert_role.id}> ` : ""} new episode`
    //     + `: ${chnl}`
    //   );
    // });
    bot.constants[teamName].forum_home.thread.send(
      `${options.alert ? `<@&${bot.constants[teamName].alert_role.id}> ` : ""} New Episode`
      + `: **${newEpisodeData.episode.title}**`
      + "\n" + newEpisodeData.episode.description
      + "\n" + newEpisodeData.episode.link
    );



  }

}

