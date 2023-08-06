import emoji
import asyncio
from discord import Message, Client
import os
import docker
from docker.types import Mount

import re

from discord_coworking.bot import MessageHandler
from dataclasses import dataclass, field


@dataclass()
class DockerRun:
    language: str
    code: str
    docker_client: docker.DockerClient = field(default_factory=docker.from_env)

    emoji = {
        'python': u'\U0001F40D',
        'java': u'\U00002615',
        'js': u'\U0001F4A9',
        'ts': u'\U0001F995',
        'php': u'\U0001F418',
        'cpp': u'\U0001F400',
        'rust': u'\U0001F980',
        'sh': u'\U0001F41A',
        'bash': u'\U0001F4BB',
        'go': u'\U0001F43F',
        'lua': u'\U0001F311',
        'ruby': u'\U00002666',
        'lisp': u'\U0001F47D',
        'perl': u'\U0001F9C5',
    }

    aliases = {
        'c++': 'cpp',
        'javascript': 'js',
        'typescript': 'ts',
    }

    images = {
        'python': 'python:3.7',
        'java': 'openjdk:11',
        'js': 'node:lts',
        'ts': 'hayd/deno',
        'php': 'php',
        'c': 'gcc',
        'cpp': 'gcc',
        'rust': 'rust',
        'sh': 'fedora',
        'bash': 'fedora',
        'go': 'golang',
        'lua': 'woahbase/alpine-lua',
        'ruby': 'ruby',
        'haskell': 'haskell',
        'lisp': 'daewok/lisp-devel',
        'perl': 'perl',
    }

    commands = {
        'python': 'python {}',
        'java': 'java {}',
        'js': 'node {}',
        'ts': 'deno run -q {}',
        'php': 'php {}',
        'c': '/bin/bash -c "gcc {} -o /tmp/a.out;/tmp/a.out"',
        'cpp': '/bin/bash -c "gcc -x c++ {} -lstdc++ -o /tmp/a.out;/tmp/a.out"',
        'rust': '/bin/bash -c "rustc {} -o /tmp/a.out;/tmp/a.out"',
        'sh': '/bin/sh {}',
        'bash': '/bin/bash {}',
        'go': 'go run {}',
        'lua': 'lua {}',
        'ruby': 'ruby {}',
        'haskell': 'runghc {}',
        'lisp': 'sbcl --script {}',
        'perl': 'perl {}',
    }

    scripts = {
        'python': 'script.py',
        'java': 'Script.java',
        'js': 'script.js',
        'ts': 'script.ts',
        'php': 'script.php',
        'c': 'script.c',
        'cpp': 'script.cpp',
        'rust': 'script.rs',
        'sh': 'script.sh',
        'bash': 'script.sh',
        'go': 'script.go',
        'lua': 'script.lua',
        'ruby': 'script.rb',
        'haskell': 'script.hs',
        'lisp': 'script.lisp',
        'perl': 'script.pl',
    }

    async def __call__(self, client: Client, message: Message):
        try:
            language = self.aliases.get(self.language, self.language)
            image = self.images.get(language)
            command = self.commands.get(language)
            script = self.scripts.get(language)
            if None in [image, command, script]:
                return
            await message.add_reaction(self.emoji.get(language, u'\U00002699'))
            volume = f'/tmp/discord-coworking-{message.id}/'
            os.mkdir(volume)
            with open(os.path.join(volume, script), 'w+') as output:
                output.write(self.code)
            container = self.docker_client.containers.run(
                image,
                command.format(os.path.join(volume, script)),
                auto_remove=False,
                network='none',
                mounts=[
                    Mount(source=volume, target=volume, type='bind')
                ],
                detach=True
            )
            await message.add_reaction(u'\U0000231B')
            running = True
            while running:
                try:
                    result = container.wait(timeout=0.01)
                    running = False
                except:
                    await asyncio.sleep(0.5)
            stdout = container.logs()
            container.remove()
            if result['StatusCode'] != 0:
                raise Exception(stdout.decode())
            await message.add_reaction(u'\U00002705')
            await message.reply(stdout.decode())
        except Exception as ex:
            await message.add_reaction(u'\U0000274C')
            await message.reply(f'```{ex.args[0]}```')
        finally:
            await message.remove_reaction(u'\U0000231B', client.user)


class RunCodeInDocker(MessageHandler):
    pattern = re.compile('```(?P<language>[a-zA-Z0-9+#-]+)\\n(?P<code>[^`]*)```')

    def accept(self, message: Message) -> bool:
        match = self.pattern.findall(message.clean_content)
        return bool(match)

    async def handle(self, client: Client, message: Message):
        for match in self.pattern.findall(message.clean_content):
            language, code = match
            run = DockerRun(language=language, code=code)
            loop = asyncio.get_event_loop()
            await asyncio.get_event_loop().run_in_executor(None, loop.create_task, run(client, message))
