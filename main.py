import discord
from discord.ext import commands
import asyncio
import os
import logging
from barry_character import BarryCharacter
from config import BARRY_RESPONSES
import threading
from web_interface import create_app

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot setup with necessary intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize Barry character
barry = BarryCharacter()

@bot.event
async def on_ready():
    """Event triggered when bot successfully connects to Discord"""
    logger.info(f'{bot.user} has connected to Discord!')
    logger.info(f'Bot is ready and serving in {len(bot.guilds)} guilds')
    
    # Set bot status
    activity = discord.Activity(type=discord.ActivityType.watching, name="for soldiers to rescue")
    await bot.change_presence(activity=activity)

@bot.event
async def on_message(message):
    """Handle incoming messages"""
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    
    # Process commands first
    await bot.process_commands(message)
    
    # Check if bot is mentioned or if it's a DM
    bot_mentioned = bot.user in message.mentions
    is_dm = isinstance(message.channel, discord.DMChannel)
    
    # Only respond if mentioned/DM AND it's not a command
    if (bot_mentioned or is_dm) and not message.content.startswith('!'):
        try:
            # Show typing indicator
            async with message.channel.typing():
                # Get Barry's response using Gemini AI
                response = await barry.get_response(
                    message.content, 
                    message.author.display_name,
                    str(message.author.id)
                )
            
            # Send response with reference to original message
            if response:
                await message.reply(response, mention_author=False)
            else:
                await message.reply("*adjusts winch controls nervously* Sorry mate, something's gone wrong with the platform controls!", mention_author=False)
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            await message.reply("*bangs on winch mechanism* Blimey, the platform's stuck! Give me a moment to sort this out!", mention_author=False)

@bot.command(name='barry')
async def barry_info(ctx):
    """Display information about Barry"""
    embed = discord.Embed(
        title="Barry - Winch Operator, 5th Regiment of Foot",
        description="*Cheerfully adjusts his cap*",
        color=0x8B4513  # Brown color representing his uniform
    )
    
    embed.add_field(
        name="About Me",
        value="Hello there! I'm Barry, your friendly winch operator. I work the platform that brings our brave lads to safety from the docks below.",
        inline=False
    )
    
    embed.add_field(
        name="Service",
        value="5th Regiment of Foot - proudly serving aboard HMS Undaunted",
        inline=True
    )
    
    embed.add_field(
        name="Location",
        value="San Sebastián Platform Operations",
        inline=True
    )
    
    embed.add_field(
        name="Duty",
        value="*salutes* Ready to lower the platform for French, Portuguese, British, and Spanish soldiers!",
        inline=False
    )
    
    embed.set_footer(text="Just mention me in a message or send me a DM to chat!")
    
    await ctx.send(embed=embed)

@bot.command(name='platform')
async def platform_status(ctx):
    """Check platform status"""
    responses = [
        "*checks winch mechanism* Platform's in good working order, ready to bring the lads up!",
        "*oils the gears* All systems operational! Platform ready for immediate deployment!",
        "*tests the ropes* Everything's shipshape down here - platform's ready when you are!",
        "*adjusts pulleys* Platform's primed and ready for our brave soldiers!",
        "*examines platform carefully* All clear! Ready to hoist our boys to safety!"
    ]
    
    import random
    response = random.choice(responses)
    await ctx.send(response)

@bot.command(name='rescue')
async def rescue_call(ctx):
    """Emergency rescue procedure"""
    response = """*immediately springs into action* 

Right then! Emergency rescue protocol activated!

*rapidly works the winch controls*

🔧 Lowering platform now!
⚙️ All systems operational!
🪖 Ready for French, Portuguese, British, and Spanish soldiers!

*calls out cheerfully* Come on lads, quick as you can! Barry's got you covered! 

*continues working the winch with determination* Don't worry mates, I'll get every last one of you to safety aboard HMS Undaunted!"""
    
    await ctx.send(response)

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandNotFound):
        # Don't respond to unknown commands to avoid spam
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("*scratches head* I'm not quite sure what you're asking there, mate. Try again?")
    else:
        logger.error(f"Command error: {error}")
        await ctx.send("*fidgets with winch controls* Something's gone a bit wrong here, but I'll keep trying!")

def run_web_interface(port=5000):
    """Run the web interface in a separate thread"""
    app = create_app()
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def main():
    """Main function to run the bot"""
    # Get Discord token from environment
    discord_token = os.getenv('DISCORD_BOT_TOKEN')
    
    if not discord_token:
        logger.error("DISCORD_BOT_TOKEN environment variable not found!")
        logger.error("Please set your Discord bot token in the environment variables.")
        return
    
    # Get Gemini API key to verify it's available
    gemini_key = os.getenv('GEMINI_API_KEY')
    if not gemini_key:
        logger.warning("GEMINI_API_KEY not found - Barry will use fallback responses")
    else:
        logger.info("Gemini AI integration enabled")
    
    # Get port from environment (Render provides this)
    port = int(os.getenv('PORT', 5000))
    
    # Start web interface in background thread with correct port
    web_thread = threading.Thread(target=lambda: run_web_interface(port), daemon=True)
    web_thread.start()
    logger.info(f"Web interface started on http://0.0.0.0:{port}")
    
    try:
        # Run the bot
        bot.run(discord_token)
    except discord.LoginFailure:
        logger.error("Failed to login to Discord. Check your bot token.")
    except Exception as e:
        logger.error(f"Error running bot: {e}")

if __name__ == "__main__":
    main()
