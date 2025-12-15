const { ContextMenuCommandBuilder, ApplicationCommandType } = require('discord.js');

module.exports = {
  data: new ContextMenuCommandBuilder()
	 .setName('DM Reminder')
   // .setDescription('Sends you a DM of the message for later')
	 .setType(ApplicationCommandType.Message),
  async execute(interaction,bot) {
		// interaction.user is the object representing the User who ran the command
		// interaction.member is the GuildMember object, which represents the user in the specific guild
    const msg = await bot.channels.cache.get(interaction.channelId).messages.fetch(interaction.targetId);
    const user = interaction.user;

    bot.functions.get('reminder').reminder(msg, user);

		await interaction.reply({content:`DMing a copy of this message to you.`, ephemeral: true});
	},
};
