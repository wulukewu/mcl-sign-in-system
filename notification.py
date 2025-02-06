import discord

def dc_send(message, token, guild_id, channel_id):

    # Set up Discord client with default intents
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        # Print login information
        print(f'We have logged in as {client.user}')

        # Get the guild (server) by ID
        guild = discord.utils.get(client.guilds, id=guild_id)

        if guild is None:
            print(f"[ERR] Guild with ID {guild_id} not found.")
            await client.close()
            return

        # Get the channel by ID
        channel = discord.utils.get(guild.channels, id=channel_id)

        if channel is None:
            print(f"[ERR] Channel with ID {channel_id} not found in guild {guild_id}.")
            await client.close()
            return

        # Send the message to the channel
        await channel.send(message)

        # Close the client after sending the message
        await client.close()

    # Run the Discord client with the provided token
    client.run(token)