from discord.ext import commands
from alfred.context import Context

class AlfredBot(commands.AutoShardedBot):
    """Custom Discord Bot class for Alfred"""

    async def process_commands(self, message):
        """Processes commands that are registed with the bot and it's groups.

        Without this being run in the main `on_message` event, commands will
        not be processed.
        """
        if message.author.bot:
            return
        ctx = await self.get_context(message, cls=Context)
        if not ctx.command:
            return
        await self.invoke(ctx)
