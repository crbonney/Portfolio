
const { SlashCommandBuilder,
        SlashCommandStringOption,
        SlashCommandChannelOption,
        ChannelType,
        PermissionFlagsBits
} = require('discord.js');
const {readFileSync, writeFileSync} = require('jsonfile'); //read/write memory JSON file
const {TESTING_MODE} = require('../bot-constants.json');

// ARUGMENTS:
// message ID
// new content for message edit
// NOTE: command must be called in the channel of the message to be edited

// TASK
// gets the message from its channel and ID
// edits its content to the new content

module.exports = {

  data: new SlashCommandBuilder()
    .setName('edit-message')
    .setDescription('Edits a message the bot posted in this channel.')
    .setDefaultMemberPermissions(PermissionFlagsBits.Administrator)
    .setDMPermission(false)
    .addStringOption(new SlashCommandStringOption()
			.setName('message_id')
			.setDescription("The ID of the message from this channel to edit")
			.setRequired(true)
		)
		.addStringOption(new SlashCommandStringOption()
			.setName('new_content')
			.setDescription("The new conent to put in the editted message")
			.setRequired(true)
		)
  ,

  async execute(interaction, bot) {

    const msg_id = interaction.options.getString('message_id');
    const new_msg_content = interaction.options.getString('new_content');

    const msg = await interaction.channel.messages.fetch(msg_id);
    console.log(`Attempting to edit message ${msg_id}`);

    // if bot couldnt fetch message, notify and return
    if (!msg) {
      console.log("| ERROR: could not find message");
      await interaction.reply({
        content: `ERROR: I could not find the specified message. Please check the message ID is valid.`,
        ephemeral: true
      });
      return
    }

    // if bot isnt the message's author, notify and return
    if (!msg.author.equals(bot.user)) {
      await interaction.reply({
        content: `ERROR: I can only edit messages I posted`,
        ephemeral: true
      });
      console.log("| ERROR: could not edit message, bot did not post it.")
      return
    }

    // else, edit message with new content
    msg.edit(new_msg_content);

    // grab thread option (if given), and check if it already exists in memory
    await interaction.reply({
      content: `Edited message.`,
      ephemeral: true
    });

  }

}
