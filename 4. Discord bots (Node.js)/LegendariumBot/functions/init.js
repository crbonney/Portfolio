
module.exports = {

  name: "init",

  // initializes legendarium server information into bot
  legendarium_data: async function(bot) {

    // get legendarium server
    bot.constants.legendarium.server = await bot.guilds.cache.get(bot.constants.legendarium.id);
    // just need introductions id for welcome message, dont need to store channel
    bot.constants.legendarium.introductions.channel = await bot.constants.legendarium.server.channels.cache.get(bot.constants.legendarium.introductions.id);

    // just need rules channel to get react role message, can unsave it after
    const rules_channel = await bot.constants.legendarium.server.channels.cache.get(bot.constants.legendarium.rules.id);
    bot.constants.legendarium.react_roles.message = await rules_channel.fetch(bot.constants.legendarium.react_roles.id);
    
    // general channel for guildMemberAdd messages
    bot.constants.legendarium.general.channel = await bot.constants.legendarium.server.channels.cache.get(bot.constants.legendarium.general.id)

    // fetch members to ensure they are in cache
    bot.constants.legendarium.server.members.fetch();

    // get episode post forum channels and their home thread
    bot.constants.greenTeam.forum.channel = await bot.constants.legendarium.server.channels.cache.get(bot.constants.greenTeam.forum.id);
    bot.constants.greenTeam.forum_home.thread = await bot.constants.legendarium.server.channels.cache.get(bot.constants.greenTeam.forum_home.id);

    bot.constants.mainTeam.forum.channel = await bot.constants.legendarium.server.channels.cache.get(bot.constants.mainTeam.forum.id);
    bot.constants.mainTeam.forum_home.thread = await bot.constants.legendarium.server.channels.cache.get(bot.constants.mainTeam.forum_home.id);

    bot.constants.rabbitPen.forum.channel = await bot.constants.legendarium.server.channels.cache.get(bot.constants.rabbitPen.forum.id);
    bot.constants.rabbitPen.forum_home.thread = await bot.constants.legendarium.server.channels.cache.get(bot.constants.rabbitPen.forum_home.id);

    // set interval to check for new episodes
    setInterval(async () => {
      await bot.functions.get('updateXML').execute(bot,"greenTeam");
      await bot.functions.get('updateXML').execute(bot,"mainTeam");
    }, bot.constants.HOUR)
  },

  community_test_data: async function(bot) {

    bot.constants.communityTest.server = await bot.guilds.cache.get(bot.constants.communityTest.id);
    // fetches members of Guild to put into bot cache
    bot.constants.communityTest.server.members.fetch();

    // get test episode post forum channel and its home thread
    bot.constants.communityTest.forum.channel = await bot.constants.communityTest.server.channels.cache.get(bot.constants.communityTest.forum.id);
    bot.constants.communityTest.forum_home.thread = await bot.constants.communityTest.server.channels.cache.get(bot.constants.communityTest.forum_home.id);

    // set fake greenTeam and mainTeam forums/channels in communityTest server
    bot.constants.greenTeam.forum.channel = await bot.constants.communityTest.server.channels.cache.get(bot.constants.communityTest.forum.id);
    bot.constants.greenTeam.forum_home.thread = await bot.constants.communityTest.server.channels.cache.get(bot.constants.communityTest.forum_home.id);

    bot.constants.mainTeam.forum.channel = await bot.constants.communityTest.server.channels.cache.get(bot.constants.communityTest.forum.id);
    bot.constants.mainTeam.forum_home.thread = await bot.constants.communityTest.server.channels.cache.get(bot.constants.communityTest.forum_home.id);

    // set interval to check for new episodes
    setInterval(async () => {
      await bot.functions.get('updateXML').execute(bot,"greenTeam");
      await bot.functions.get('updateXML').execute(bot,"mainTeam");

    }, bot.constants.HOUR)

  }


}
