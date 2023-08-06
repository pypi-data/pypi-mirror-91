import argparse
import asyncio
import io
import logging.config
import os
import pickle

import discord

from discord_coworking.command.api import Result
from discord_coworking.command.category import DeleteCategory
from discord_coworking.command.coworking import CreateOrganization
from discord_coworking.command.guild import GuildPredicate
from discord_coworking.command.predicate import ANY
from discord_coworking.command.role import DeleteRole
from discord_coworking.command.text_channel import DeleteTextChannel
from discord_coworking.command.voice_channel import DeleteVoiceChannel

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


def config_log(log_level):
    logging.basicConfig(level=log_level)
    logging.info(f'Log level set to {log_level}')


async def run(token: str, command, log_level, **params):
    config_log(log_level)
    client = discord.Client()
    loop = asyncio.get_event_loop()
    loop.create_task(client.start(token))
    await client.wait_until_ready()
    await command(client, **params)


async def undo_command(client: discord.Client, result: io.BufferedReader, **params):
    undoable = pickle.load(result)
    if not isinstance(undoable, (Result,)):
        raise Exception('The input file is not a result')
    await undoable.undo(client)


async def discord_command(client: discord.Client, command_factory, result: io.BufferedWriter, **parameters):
    command = command_factory(**parameters)
    logging.info(f'Running command {command}')
    pickle.dump(await command.do(client), result)


async def main():
    parser = argparse.ArgumentParser(
        prog='discord-coworking',
        description='Discord coworking server management toolkit',
    )
    parser.add_argument(
        '--token',
        help='Discord Bot Token, environment DISCORD_TOKEN',
        default=os.environ.get('DISCORD_TOKEN', None),
    )
    parser.add_argument(
        '--guild',
        help='Guild ID',
        default=os.environ.get('GUILD_ID', None),
        type=lambda it: ANY if it is None else GuildPredicate.create(id=int(it))
    )
    parser.add_argument(
        '--log-level',
        help='Log level',
        default=os.environ.get('LOG_LEVEL', 'i'),
        choices=list(log_level_map.keys()),
        type=lambda it: log_level_map.get(it, logging.INFO),
    )
    parser.set_defaults(command=lambda *args, **kwargs: print(args, kwargs))
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
    namespace = parser.parse_args()
    return await run(**vars(namespace))


asyncio.get_event_loop().run_until_complete(main())
