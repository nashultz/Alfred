import asyncio
import discord
import aiohttp
import re
import aiohttp
import random
import sys
import os
import aiosocks
import time
import traceback
import inspect
import io
import math
import async_timeout
from pymysql.converters import escape_item, escape_string, encoders
from contextlib import redirect_stdout
import linecache
from discord.ext import commands
from discord.ext.commands.errors import CommandNotFound, CommandError
from discord.ext.commands.context import Context
from io import BytesIO

class DataProtocol(asyncio.SubprocessProtocol):
	def __init__(self, exit_future):
		self.exit_future = exit_future
		self.output = bytearray()

	def pipe_data_received(self, fd, data):
		self.output.extend(data)

	def process_exited(self):
		self.exit_future.set_result(True)

	def pipe_connection_lost(self, fd, exc):
		self.exit_future.set_result(True)

	def connection_lost(self, exc):
		self.exit_future.set_result(True)

class Funcs():
	def __init__(self, bot, cursor):
		self.bot = bot
		self.cursor = cursor
		self.bot.google_api_keys = open(self.discord_path('utils/keys.txt')).read().split('\n')
		self.bot.google_count = 0
		self.image_mimes = ['image/png', 'image/pjpeg', 'image/jpeg', 'image/x-icon']

	def discord_path(self, path):
		return os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), path)

	def files_path(self, path):
		return self.discord_path('files/'+path)

	async def prefix_check(self, s, prefix, prefix_set):
		if prefix_set:
			return True
		count = 0
		for x in s:
			if count == 2:
				break
			elif count == 1:
				if x != prefix:
					break
			if x == prefix:
				count += 1
		if count == 1:
			return True
		return False

	async def get_prefix(self, message):
		if self.bot.dev_mode:
			prefix = ','
		else:
			prefix = '.'
		prefix_set = False
		if message.channel.is_private is False and message.content.startswith(prefix+"prefix") is False:
			sql = "SELECT prefix FROM `prefix` WHERE server={0}"
			sql = sql.format(message.server.id)
			sql_channel = "SELECT prefix,channel FROM `prefix_channel` WHERE server={0} AND channel={1}"
			sql_channel = sql_channel.format(message.server.id, message.channel.id)
			result = self.cursor.execute(sql_channel).fetchall()
			if result:
				for s in result:
					if s['channel'] == message.channel.id:
						prefix = s['prefix']
						prefix_set = True
						break
			elif not prefix_set:
				result = self.cursor.execute(sql).fetchall()
				if len(result) != 0:
					prefix = result[0]['prefix']
					prefix_set = True
			if prefix_set:
				prefix = prefix.lower()
		mention = commands.bot.when_mentioned(self.bot, message)
		if message.content.startswith(mention):
			check = True
		else:
			check = await self.prefix_check(message.content, prefix, prefix_set)
		return [prefix, mention], check

	async def is_blacklisted(self, message):
		try:
			perms = message.channel.permissions_for(message.server.me)
			if perms.send_messages is False or perms.read_messages is False:
				return True
		except:
			pass
		if message.author.id == self.bot.owner.id:
			return False
		global_blacklist_result = self.cursor.execute('SELECT * FROM `global_blacklist` WHERE user={0}'.format(message.author.id)).fetchall()
		if message.channel.is_private:
			if len(global_blacklist_result) != 0 and message.author.id != bot.owner.id:
				return True
			return False
		muted_check_result = self.cursor.execute('SELECT * FROM `muted` WHERE server={0} AND id={1}'.format(message.server.id, message.author.id)).fetchall()
		if len(muted_check_result) != 0 and message.server.owner != message.author:
			return True
		server_blacklist_result = self.cursor.execute('SELECT * FROM `blacklist` WHERE server={0} AND user={1}'.format(message.server.id, message.author.id)).fetchall()
		channel_blacklist_result = self.cursor.execute('SELECT * FROM `channel_blacklist` WHERE server={0} AND channel={1}'.format(message.server.id, message.channel.id)).fetchall()
		if len(global_blacklist_result) != 0:
			return True
		elif len(server_blacklist_result) != 0:
			return True
		elif len(channel_blacklist_result) != 0:
			if 'blacklist' in message.content:
				return False
			return True
		return False

	async def command_check(self, message, command, prefix):
		if message.author.id == self.bot.owner.id:
			return False
		sql = 'SELECT * FROM `command_blacklist` WHERE type="global" AND command={0}'
		sql = sql.format(self.escape(command))
		result = self.cursor.execute(sql).fetchall()
		if len(result) != 0:
			return True
		if message.channel.is_private:
			return False
		sql = 'SELECT * FROM `command_blacklist` WHERE server={0}'
		sql = sql.format(message.server.id)
		result = self.cursor.execute(sql).fetchall()
		if message.channel.topic != None:
			command_escape = re.escape(command)
			topic_regex = re.compile(r"((\[|\{)"+command_escape+"(\]|\}))", re.I|re.S)
			topic_match = True if topic_regex.findall(message.channel.topic.lower()) else False
		else:
			topic_match = False
		is_admin = False
		try:
			perms = message.channel.permissions_for(message.author)
			if perms.administrator or perms.manage_server or perms.manage_roles:
				is_admin = True
		except:
			pass
		for s in result:
			if s['command'] != command:
				continue
			if s['type'] == 'server':
				if topic_match:
					return False
				else:
					await self.bot.send_message(message.channel, ':no_entry: **That command is disabled on this server**{0}'.format("\n`{0}command enable {1}` to enable the command.\n**Alternatively** place `[{1}]` in the channel topic or name.".format(prefix, command) if is_admin else ''))
					return True
			elif s['type'] == 'channel':
				if str(s['channel']) == str(message.channel.id):
					await self.bot.send_message(message.channel, ':no_entry: **That command is disabled in this channel**{0}'.format("\n`{0}command enable channel {1}` {2} to enable the command.".format(prefix, command, message.channel.mention) if is_admin else ''))
					return True
			elif s['type'] == 'role':
				for role in message.author.roles:
					if str(role.id) == str(s['role']):
						await self.bot.send_message(message.channel, ':no_entry: **That command is disabled for role: {1}**{0}'.format("\n`{0}command enable channel {1}` {2} to enable the command.".format(prefix, command, role.mention) if is_admin else ''), role.mention)
						return True
			elif s['type'] == 'user':
				if str(s['user']) == str(message.author.id):
					return True
		return False

	async def process_commands(self, message, command, prefix):
		_internal_channel = message.channel
		_internal_author = message.author
		view = commands.view.StringView(message.content)
		view.skip_string(prefix)
		invoker = view.get_word()
		tmp = {
			'bot': self.bot,
			'invoked_with': invoker,
			'message': message,
			'view': view,
			'prefix': prefix
		}
		ctx = Context(**tmp)
		del tmp
		try:
			command = self.bot.commands[command]
		except:
			raise Exception('wot')
		self.bot.dispatch('command', command, ctx)
		try:
			with async_timeout.timeout(60):
				await command.invoke(ctx)
		except CommandError as e:
			ctx.command.dispatch_error(e, ctx)
		except asyncio.TimeoutError:
			await self.bot.send_message(message.channel, ':warning: **Command timed out, don\'t be an asshole.**')
			return
		else:
			self.bot.dispatch('command_completion', command, ctx)

	async def queue_message(self, channel_id:str, msg:str):
		message_id = random.randint(0, 1000000)
		payload = {'key':'keeee', 'id': message_id, 'channel_id': channel_id, 'message': msg}
		try:
			with aiohttp.ClientSession() as session:
				with aiohttp.Timeout(15):
					async with session.post('http://no:2221/queue', data=payload) as r:
						pass
		except (asyncio.TimeoutError, aiohttp.errors.ClientConnectionError, aiohttp.errors.ClientError):
			await asyncio.sleep(5)
			return

	async def isimage(self, url:str):
		try:
			with aiohttp.ClientSession() as session:
				with aiohttp.Timeout(5):
					async with session.get(url) as resp:
						if resp.status == 200:
							mime = resp.headers.get('Content-type', '').lower()
							if any([mime == x for x in self.image_mimes]):
								return True
							else:
								return False
		except:
			return False

	async def isgif(self, url:str):
		try:
			with aiohttp.ClientSession() as session:
				with aiohttp.Timeout(5):
					async with session.get(url) as resp:
						if resp.status == 200:
							mime = resp.headers.get('Content-type', '').lower()
							if mime == "image/gif":
								return True
							else:
								return False
		except:
			return False

	async def download(self, url:str, path:str):
		try:
			with aiohttp.ClientSession() as session:
				with aiohttp.Timeout(5):
					async with session.get(url) as resp:
						data = await resp.read()
						with open(path, "wb") as f:
							f.write(data)
		except asyncio.TimeoutError:
			return False

	async def bytes_download(self, url:str):
		try:
			with aiohttp.ClientSession() as session:
				with aiohttp.Timeout(5):
					async with session.get(url) as resp:
						data = await resp.read()
						b = BytesIO(data)
						b.seek(0)
						return b
		except asyncio.TimeoutError:
			return False

	async def get_json(self, url:str):
		try:
			with aiohttp.ClientSession() as session:
				with aiohttp.Timeout(5):
					async with session.get(url) as resp:
						try:
							load = await resp.json()
							return load
						except:
							return {}
		except asyncio.TimeoutError:
			return {}

	async def run_process(self, code, response=False):
		try:
			loop = self.bot.loop
			exit_future = asyncio.Future(loop=loop)
			create = loop.subprocess_exec(lambda: DataProtocol(exit_future),
																		*code, stdin=None, stderr=None)
			transport, protocol = await asyncio.wait_for(create, timeout=30)
			await exit_future
			transport.close()
			if response:
				data = bytes(protocol.output)
				return data.decode('ascii').rstrip()
			return True
		except asyncio.TimeoutError:
			return False

	async def proxy_request(self, url, **kwargs):
		post = kwargs.get('post')
		post = True if post != {} else False
		post_data = kwargs.get('post_data')
		headers = kwargs.get('headers')
		j = kwargs.get('j')
		j = True if j != {} else False
		proxy_addr = aiosocks.Socks5Addr('proxy-nl.privateinternetaccess.com', 1080)
		proxy_auth = aiosocks.Socks5Auth('', password='')
		proxy_connection = aiosocks.connector.SocksConnector(proxy=proxy_addr, proxy_auth=proxy_auth, remote_resolve=True)
		with aiohttp.ClientSession(connector=proxy_connection) as session:
			async with session.post(url, data=post_data if post else None, headers=headers) as resp:
				if j:
					return await resp.json()
				else:
					return await resp.text()

	async def truncate(self, channel, msg):
		if len(msg) == 0:
			return
		split = [msg[i:i + 1999] for i in range(0, len(msg), 1999)]
		try:
			for s in split:
				await self.bot.send_message(channel, s)
				await asyncio.sleep(0.21)
		except Exception as e:
			await self.bot.send_message(channel, e)

	async def get_images(self, ctx, **kwargs):
		try:
			message = ctx.message
			channel = ctx.message.channel
			attachments = ctx.message.attachments
			mentions = ctx.message.mentions
			limit = kwargs.pop('limit', None)
			urls = kwargs.pop('urls', [])
			gif = kwargs.pop('gif', False)
			if gif:
				check_func = self.isgif
			else:
				check_func = self.isimage
			if urls is None:
				urls = []
			elif type(urls) != tuple:
				urls = [urls]
			else:
				urls = list(urls)
			scale = kwargs.pop('scale', None)
			scale_msg = None
			int_scale = None
			if gif is False:
				for mention in mentions:
					urls.append(mention.avatar_url)
					if limit:
						limit += 1
			for attachment in attachments:
				urls.append(attachment['url'])
			if scale:
				scale_limit = scale
				if limit:
					limit += 1
			if limit and urls and len(urls) > limit:
				await self.bot.send_message(channel, ':no_entry: `Max image limit (<= {0})`'.format(limit))
				ctx.command.reset_cooldown(ctx)
				return False
			img_urls = []
			count = 1
			for url in urls:
				if url.startswith('<@'):
					continue
				try:
					if scale:
						if str(math.floor(float(url))).isdigit():
							int_scale = int(math.floor(float(url)))
							scale_msg = '`Scale: {0}`\n'.format(int_scale)
							if int_scale > scale_limit and ctx.message.author.id != self.bot.owner.id:
								int_scale = scale_limit
								scale_msg = '`Scale: {0} (Limit: <= {1})`\n'.format(int_scale, scale_limit)
							continue
				except:
					pass
				check = await check_func(url)
				if check is False and gif is False:
					check = await self.isgif(url)
					if check:
						await self.bot.send_message(channel, ":warning: This command is for images, not gifs (use `gmagik` or `gascii`)!")
						ctx.command.reset_cooldown(ctx)
						return False
					elif len(img_urls) == 0:
						await self.bot.send_message(channel, 'Invalid or Non-Image(s)!')
						ctx.command.reset_cooldown(ctx)
						return False
					else:
						await self.bot.send_message(channel, ':warning: Image `{0}` is Invalid!'.format(count))
						continue
				elif gif and check is False:
					check = await self.isimage(url)
					if check:
						await self.bot.send_message(channel, ":warning: This command is for gifs, not images (use `magik`)!")
						ctx.command.reset_cooldown(ctx)
						return False
					elif len(img_urls) == 0:
						await self.bot.send_message(channel, 'Invalid or Non-Gifs(s)!')
						ctx.command.reset_cooldown(ctx)
						return False
					else:
						await self.bot.send_message(channel, ':warning: Gif `{0}` is Invalid!'.format(count))
						continue
				img_urls.append(url)
				count += 1
			else:
				if len(img_urls) == 0:
					last_attachment = None
					async for m in self.bot.logs_from(channel, before=message, limit=25):
						check = False
						if m.attachments:
							last_attachment = m.attachments[0]['url']
							check = await check_func(last_attachment)
						elif m.embeds:
							last_attachment = m.embeds[0]['url']
							check = await check_func(last_attachment)
						if check:
							img_urls.append(last_attachment)
							break
						else:
							continue
					if len(img_urls) == 0:
						await self.bot.send_message(channel, ":no_entry: Please input url(s){0}or attachment(s).".format(', mention(s) ' if not gif else ' '))
						ctx.command.reset_cooldown(ctx)
						return False
			if scale:
				return img_urls, int_scale, scale_msg
			return img_urls
		except Exception as e:
			print(e)

	async def google_keys(self):
		keys = self.bot.google_api_keys
		if self.bot.google_count >= len(keys):
			self.bot.google_count = 0
		key = keys[self.bot.google_count]
		self.bot.google_count += 1
		return str(key)

	def write_last_time(self):
		path = self.files_path('last_time_{0}.txt'.format(self.bot.shard_id))
		utc = str(int(time.time()))
		with open(path, 'wb') as f:
			f.write(utc.encode())
			f.close()

	def get_last_time(self):
		path = self.files_path('last_time_{0}.txt'.format(self.bot.shard_id))
		try:
			return int(open(path, 'r').read())
		except:
			return False

	def restart_program(self):
		python = sys.executable
		os.execl(python, python, * sys.argv)

	async def cleanup_code(self, content):
		"""Automatically removes code blocks from the code."""
		if content.startswith('```') and content.endswith('```'):
			clean = '\n'.join(content.split('\n')[1:-1])
		else:
			clean = content.strip('` \n')
		if clean.startswith('http'):
			with aiohttp.ClientSession() as session:
				async with session.get(clean) as r:
					code = await r.text()
			clean = code
		return clean

	def get_syntax_error(self, e):
		return '```py\n{0.text}{1:>{0.offset}}\n{2}: {0}```'.format(e, '^', type(e).__name__)

	async def repl(self, ctx, code):
		msg = ctx.message
		variables = {
				'ctx': ctx,
				'bot': self.bot,
				'message': msg,
				'server': msg.server,
				'channel': msg.channel,
				'author': msg.author,
				'last': None,
				'commands': commands,
				'discord': discord,
				'asyncio': asyncio,
				'cursor': self.cursor
		}
		cleaned = await self.cleanup_code(code)
		if cleaned in ('quit', 'exit', 'exit()'):
			await self.bot.say('Exiting.')
			return 'exit'
		executor = exec
		if cleaned.count('\n') == 0:
			try:
				code = compile(cleaned, '<repl session>', 'eval')
			except SyntaxError:
				pass
			else:
				executor = eval
		if executor is exec:
			try:
				code = compile(cleaned, '<repl session>', 'exec')
			except SyntaxError as e:
				await self.bot.say(self.get_syntax_error(e))
				return False
		fmt = None
		stdout = io.StringIO()
		try:
			with redirect_stdout(stdout):
				result = executor(code, variables)
				if inspect.isawaitable(result):
					result = await result
		except Exception as e:
			value = stdout.getvalue()
			fmt = '```py\n{}{}\n```'.format(value, traceback.format_exc())
		else:
			value = stdout.getvalue()
			if result is not None:
				fmt = '```py\n{}{}\n```'.format(value, result)
				variables['last'] = result
			elif value:
				fmt = '```py\n{}\n```'.format(value)
		return fmt

	async def command_help(self, ctx):
		if ctx.invoked_subcommand:
			cmd = ctx.invoked_subcommand
		else:
			cmd = ctx.command
		pages = self.bot.formatter.format_help_for(ctx, cmd)
		for page in pages:
			await self.bot.send_message(ctx.message.channel, page.replace("\n", "fix\n", 1))

	def escape(self, obj, mapping=encoders):
		if isinstance(obj, str):
			return "'" + escape_string(obj) + "'"
		return escape_item(obj, 'utf8mb4', mapping=mapping)

# async def is_above(ctx, user):
# 	u1 = ctx.author
# 	if u1 == bot.owner:
# 		return True
# 	u2 = user
# 	server = ctx.message.server
# 	channel = ctx.message.channel
# 	if server.owner == u1:
# 		return True
# 	elif server.owner == u2:
# 		return '`User is the server owner.`'
# 	if channel.permissions_for(u1).administrator and channel.permissions_for(u2).administrator and u1.top_role.position > u2.top_role.position:
# 		return True
# 	elif u1.top_role == u2.top_role:
# 		return '`Same role.`'
# 	if u1.top_role.position > u2.top_role.position:
# 		return True