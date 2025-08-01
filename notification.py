import os
import ssl
import certifi

# Set SSL certificate path before importing discord
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['SSL_CERT_DIR'] = certifi.where()

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

    # Run the Discord client
    try:
        client.run(token)
    except Exception as e:
        print(f"[ERR] Failed to send Discord notification: {e}")
        # Fallback: try with disabled SSL verification
        try:
            # Disable SSL verification
            ssl._create_default_https_context = ssl._create_unverified_context
            client.run(token)
        except Exception as e2:
            print(f"[ERR] Failed to send Discord notification (fallback): {e2}")