
const { SlashCommandBuilder, PermissionFlagsBits} = require('discord.js');

module.exports = {

  data: new SlashCommandBuilder()
    .setName('restart')
    .setDescription('Restarts the bot.')
    .setDefaultMemberPermissions(PermissionFlagsBits.Administrator)
    .setDMPermission(false),

  async execute(interaction, bot) {
    await interaction.reply({
      content: `Restarting bot`,
      ephemeral: true
    });

    process.exit(1);

  }
}
