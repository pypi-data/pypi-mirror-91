import asyncio
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
import argparse
import asyncio
import io
import logging.config
import os
import pickle
from asyncio.tasks import Task

import discord

from discord.message import Message
from discord_coworking.command.api import Result
from discord_coworking.command.category import DeleteCategory
from discord_coworking.command.coworking import CreateOrganization
from discord_coworking.command.guild import GuildPredicate
from discord_coworking.command.predicate import ANY
from discord_coworking.command.role import DeleteRole
from discord_coworking.command.text_channel import DeleteTextChannel
from discord_coworking.command.voice_channel import DeleteVoiceChannel
from discord_coworking.bot import CoworkingBot
from discord_coworking.bot.handler.run_in_docker import RunCodeInDocker

log_level_map = {
    'd': 'DEBUG',
    'debug': 'DEBUG',
    'i': 'INFO',
    'info': 'INFO',
    'w': 'WARNING',
    'warning': 'WARNING',
    'c': 'CRITICAL',
    'critical': 'CRITICAL',
}


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='discord-coworking',
        description='Discord coworking server management toolkit',
    )
    parser.add_argument(
        '--token',
        help='Discord Bot Token, environment DISCORD_TOKEN',
        **default_env('DISCORD_TOKEN', str, None),
    )
    parser.add_argument(
        '--guild',
        help='Guild ID',
        **default_env('GUILD_ID', lambda it: GuildPredicate.create(id=int(it)), ANY)
    )
    parser.add_argument(
        '--log-level',
        help='Log level',
        default=os.environ.get('LOG_LEVEL', 'i'),
        choices=list(log_level_map.keys()),
        type=lambda it: log_level_map.get(it, logging.INFO),
    )
    parser.set_defaults(
        client_factory=discord.Client,
        command=lambda *args, **kwargs: print(args, kwargs),
    )
    subparsers = parser.add_subparsers(
        title='sub command',
    )
    undo = subparsers.add_parser(
        'undo',
    )
    undo.add_argument(
        'result',
        help='Serialized result file',
        type=argparse.FileType('rb'),
    )
    undo.set_defaults(command=undo_command)
    bot = subparsers.add_parser(
        'bot',
    )
    bot.set_defaults(
        client_factory=CoworkingBot,
        command=run_bot,
    )
    create_organization_commands = {
        'create-open-organization': CreateOrganization.open_organization,
        'create-private-organization': CreateOrganization.private_organization,
    }
    for name, factory in create_organization_commands.items():
        create_organization = subparsers.add_parser(
            name,
        )
        create_organization.add_argument(
            '--result',
            default='a.out',
            type=argparse.FileType('wb+'),
        )
        create_organization.add_argument(
            '--name',
            required=True,
        )
        create_organization.set_defaults(
            command=discord_command,
            command_factory=factory,
        )
    delete_commands = {
        'delete-category': DeleteCategory,
        'delete-voice-channel': DeleteVoiceChannel,
        'delete-text-channel': DeleteTextChannel,
        'delete-role': DeleteRole,
    }
    for name, factory in delete_commands.items():
        create_organization = subparsers.add_parser(
            name,
        )
        create_organization.add_argument(
            '--result',
            default='a.out',
            type=argparse.FileType('wb+'),
        )
        create_organization.set_defaults(
            command=discord_command,
            command_factory=factory,
        )
    list_commands = {
        'list-guild': None,
    }
    for name, _ in list_commands.items():
        command = subparsers.add_parser(
            name,
        )
        command.set_defaults(
            command=list_command,
        )
    return parser


def config_log(log_level):
    logging.basicConfig(level=log_level)
    logging.info(f'Log level set to {log_level}')


async def run(token: str, client_factory, command, log_level, **params):
    config_log(log_level)
    client = client_factory()
    loop = asyncio.get_event_loop()
    client_task = loop.create_task(client.start(token))
    await client.wait_until_ready()
    await command(client, **params, client_task=client_task)


async def list_command(client: discord.Client, **params):
    for guild in client.guilds:
        print(f'"{guild.name}" ({guild.id})')


async def print_handler(client, message):
    print(message)


async def reply_handler(client, message: Message):
    await message.reply(message.clean_content)


async def run_bot(client: CoworkingBot, client_task: Task, **params):
    client.message_handler.handlers.extend([
        RunCodeInDocker(),
    ])
    await client_task


async def undo_command(client: discord.Client, result: io.BufferedReader, **params):
    undoable = pickle.load(result)
    if not isinstance(undoable, (Result,)):
        raise Exception('The input file is not a result')
    await undoable.undo(client)


async def discord_command(client: discord.Client, command_factory, result: io.BufferedWriter, **parameters):
    command = command_factory(**parameters)
    logging.info(f'Running command {command}')
    pickle.dump(await command.do(client), result)


def default_env(name, type, default):
    env_value = os.environ.get(name, None)
    return {
        'default': default if env_value is None else type(env_value),
        'required': env_value is None and default is None,
        'type': type,
    }


async def main():
    parser = create_parser()
    namespace = parser.parse_args()
    return await run(**vars(namespace))


try:
    cpu_count = multiprocessing.cpu_count()
    thread_pool = ThreadPoolExecutor(cpu_count)
    loop = asyncio.get_event_loop()
    loop.set_default_executor(thread_pool)
    loop.run_until_complete(main())
except KeyboardInterrupt:
    asyncio.get_event_loop().close()
