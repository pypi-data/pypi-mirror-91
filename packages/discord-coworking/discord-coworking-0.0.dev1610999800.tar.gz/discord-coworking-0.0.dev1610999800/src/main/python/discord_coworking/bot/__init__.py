from discord import Client
from discord.message import Message

from discord_coworking.bot.api import MessageHandler
from discord_coworking.bot.handler import MessageHandlerChain
from discord_coworking.command.predicate import FnPredicate


class CoworkingBot(Client):
    message_handler: MessageHandlerChain

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message_handler = MessageHandlerChain(
            handlers=[],
            predicate=FnPredicate(lambda message: message.author.id != self.user.id),
        )

    async def on_message(self, message: Message):
        await self.message_handler(self, message)
