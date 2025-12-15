const { SlashCommandBuilder, PermissionFlagsBits  } = require('discord.js');

const {
  ActionRowBuilder,
  Events,
  ModalBuilder,
  TextInputBuilder,
  TextInputStyle
} = require('discord.js');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('suggestion')
		.setDefaultMemberPermissions(PermissionFlagsBits.Administrator)
    .setDMPermission(false)
		.setDescription('Allows you to privately make a suggestion to the server (example implementation here for feedback)')
    // .addSubcommand(subcommand =>
		// 	subcommand
		// 		.setName('user')
		// 		.setDescription('Info about a user')
		// 		.addUserOption(option => option.setName('target').setDescription('The user')))
		// .addSubcommand(subcommand =>
		// 	subcommand
		// 		.setName('server')
		// 		.setDescription('Info about the server')),
		,
	async execute(interaction,bot) {
		// await interaction.reply('Pong!');


		      const modal = new ModalBuilder()
		        .setCustomId('suggestionModal')
		  			.setTitle('Server Suggestion');

				// Create the text input components
				const titleInput = new TextInputBuilder()
					.setCustomId('titleInput')
				    // The label is the prompt the user sees for this input
					.setLabel("What suggestion do you have?")
				    // Short means only a single line of text
					.setStyle(TextInputStyle.Short);

				const longInput = new TextInputBuilder()
					.setCustomId('longInput')
					.setLabel("Why do you think this would be interesting?")
				    // Paragraph means multiple lines of text.
					.setStyle(TextInputStyle.Paragraph);

				// An action row only holds one text input,
				// so you need one action row per text input.
				const firstActionRow = new ActionRowBuilder().addComponents(titleInput);
				const secondActionRow = new ActionRowBuilder().addComponents(longInput);

				// Add inputs to the modal
				modal.addComponents(firstActionRow, secondActionRow);

				// Show the modal to the user
				await interaction.showModal(modal);
	},
};
