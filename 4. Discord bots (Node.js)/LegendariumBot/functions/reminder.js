const {emojis} = require('../bot-constants.json');

module.exports = {

  name: "reminder",
  description: "given a message and user, sends a copy of that message to the user as DM",

  reminder: async function (msg, user) {

    let attachment_urls = "";
    if (msg.attachments) {
      for (let file of msg.attachments.entries()) {
        attachment_urls += `\n ${file[1].url}`;
      }

    }
    user.send(`${msg.url} from ${msg.author}: \n${msg.content} ${attachment_urls}`).then(m => {
      m.react(emojis.delete_dm_emoji);
    });

    console.log(`Sending reaction reminder to ${user.username}, from ${msg.channel.name}`);
  }

}
