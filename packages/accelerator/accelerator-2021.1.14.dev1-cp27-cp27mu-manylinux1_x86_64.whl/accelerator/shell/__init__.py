############################################################################
#                                                                          #
# Copyright (c) 2019-2020 Carl Drougge                                     #
# Modifications copyright (c) 2020 Anders Berkeman                         #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License");          #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#  http://www.apache.org/licenses/LICENSE-2.0                              #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
#                                                                          #
############################################################################

from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import sys
import errno
from os import getcwd, chdir
from os.path import dirname, basename, realpath, join
import locale
from glob import glob
import shlex
from argparse import RawDescriptionHelpFormatter

from accelerator.compat import ArgumentParser
from accelerator.error import UserError

cfg = None

def find_cfgs(basedir='.', wildcard=False):
	"""Find all accelerator.conf (or accelerator*.conf if wildcard=True)
	starting at basedir and continuing all the way to /, yielding them
	from the deepest directory first, starting with accelerator.conf (if
	present) and then the rest in sorted order."""

	cfgname = 'accelerator.conf'
	if wildcard:
		pattern = 'accelerator*.conf'
	else:
		pattern = cfgname
	orgdir = getcwd()
	basedir = realpath(basedir)
	while basedir != '/':
		try:
			chdir(basedir)
			fns = sorted(glob(pattern))
		finally:
			chdir(orgdir)
		if cfgname in fns:
			fns.remove(cfgname)
			fns.insert(0, cfgname)
		for fn in fns:
			yield join(basedir, fn)
		basedir = dirname(basedir)

def load_some_cfg(basedir='.', all=False):
	global cfg

	basedir = realpath(basedir)
	cfgs = find_cfgs(basedir, wildcard=all)
	if all:
		found_any = False
		# Start at the root, so closer cfgs override those further away.
		for fn in reversed(list(cfgs)):
			try:
				load_cfg(fn)
				found_any = True
			except Exception:
				# As long as we find at least one we're happy.
				pass
		if not found_any:
			raise UserError("Could not find 'accelerator*.conf' in %r or any of its parents." % (basedir,))
	else:
		try:
			fn = next(cfgs)
		except StopIteration:
			raise UserError("Could not find 'accelerator.conf' in %r or any of its parents." % (basedir,))
		load_cfg(fn)

def load_cfg(fn):
	global cfg

	from accelerator.configfile import load_config
	from accelerator.job import WORKDIRS

	cfg = load_config(fn)
	for k, v in cfg.workdirs.items():
		if WORKDIRS.get(k, v) != v:
			print("WARNING: %s overrides workdir %s" % (fn, k,), file=sys.stderr)
		WORKDIRS[k] = v
	return cfg

def unpath(path):
	while path in sys.path:
		sys.path.pop(sys.path.index(path))

def setup(config_fn=None, debug_cmd=False):
	try:
		locale.resetlocale()
	except locale.Error:
		print("WARNING: Broken locale", file=sys.stderr)
	# Make sure the accelerator dir in not in sys.path
	# (as it might be if running without installing.)
	unpath(dirname(__file__))
	if config_fn is False:
		return
	user_cwd = getcwd()
	if config_fn:
		load_cfg(config_fn)
	else:
		load_some_cfg(all=debug_cmd)
	cfg.user_cwd = user_cwd
	if not debug_cmd:
		# We want the project directory to be first in sys.path.
		unpath(cfg['project_directory'])
		sys.path.insert(0, cfg['project_directory'])
		# For consistency we also always want the project dir
		# as working directory.
		chdir(cfg['project_directory'])

def cmd_grep(argv):
	from accelerator.shell.grep import main
	return main(argv, cfg)
cmd_grep.help = '''search for a pattern in one or more datasets'''
cmd_grep.is_debug = True

def cmd_ds(argv):
	from accelerator.shell.ds import main
	return main(argv, cfg)
cmd_ds.help = '''display information about datasets'''
cmd_ds.is_debug = True

def cmd_run(argv):
	from accelerator.build import main
	return main(argv, cfg)
cmd_run.help = '''run a build script'''

def cmd_abort(argv):
	parser = ArgumentParser(prog=argv.pop(0))
	parser.add_argument('-q', '--quiet', action='store_true', help="no output")
	args = parser.parse_args(argv)
	from accelerator.build import Automata
	a = Automata(cfg.url)
	res = a.abort()
	if not args.quiet:
		print("Killed %d running job%s." % (res.killed, '' if res.killed == 1 else 's'))
cmd_abort.help = '''abort running job(s)'''

def cmd_server(argv):
	from accelerator.server import main
	from accelerator.methods import MethodLoadException
	try:
		main(argv, cfg)
	except MethodLoadException as e:
		print(e)
cmd_server.help = '''run the main server'''

def cmd_init(argv):
	from accelerator.shell.init import main
	main(argv)
cmd_init.help = '''create a project directory'''

def cmd_urd(argv):
	from accelerator.urd import main
	main(argv, cfg)
cmd_urd.help = '''run the urd server'''

def cmd_curl(argv):
	prog = argv.pop(0)
	if argv and argv[0] in ('server', 'urd',):
		which = argv.pop(0)
	else:
		which = 'urd'
	if '--help' in argv or '-h' in argv or not argv:
		from os import environ
		fh = sys.stdout if argv else sys.stderr
		print('usage: %s [server|urd] [curl options] path' % (prog,), file=fh)
		print('%s server talks to the server, %s urd talks to urd (default)' % (prog, prog,), file=fh)
		print(file=fh)
		print('examples:', file=fh)
		print('  %s %s/example/latest' % (prog, environ['USER'],), file=fh)
		print('  %s server status' % (prog,), file=fh)
		return
	url_end = argv.pop()
	socket_opts = []
	if which == 'urd':
		url_start = cfg.urd
	else: # server
		url_start = cfg.url
	if url_start.startswith('unixhttp://'):
		from accelerator.compat import unquote_plus
		url_start = url_start.split('://', 1)[1]
		if '/' in url_start:
			socket, url_start = url_start.split('/', 1)
		else:
			socket, url_start = url_start, ''
		socket_opts = ['--unix-socket', unquote_plus(socket)]
		url_start = join('http://.', url_start)
	argv = ['curl', '-s'] + socket_opts + argv + [join(url_start, url_end)]
	from subprocess import Popen, PIPE
	import json
	output, _ = Popen(argv, stdout=PIPE).communicate()
	try:
		output = output.decode('utf-8')
		output = json.dumps(json.loads(output), indent=4)
	except Exception:
		pass
	print(output)
cmd_curl.help = '''http request (with curl) to urd or the server'''

def cmd_method(argv):
	from accelerator.shell.method import main
	main(argv, cfg)
cmd_method.help = '''information about methods'''

def cmd_workdir(argv):
	from accelerator.shell.workdir import main
	main(argv, cfg)
cmd_workdir.help = '''information about workdirs'''
cmd_workdir.is_debug = True

def cmd_job(argv):
	from accelerator.shell.job import main
	return main(argv, cfg)
cmd_job.help = '''information about a job'''
cmd_job.is_debug = True

def cmd_board(argv):
	from accelerator.board import main
	main(argv, cfg)
cmd_board.help = '''runs a webserver for displaying results'''

def cmd_version(argv):
	from accelerator import __version__ as ax_version
	if len(argv) > 1:
		if argv[1:] in (['-h'], ['--help']):
			print('Usage:', argv[0])
			return 0
		else:
			print('Usage:', argv[0], file=sys.stderr)
			return 1
	else:
		print(ax_version)
cmd_version.help = '''show installed accelerator version'''

COMMANDS = dict(
	ds=cmd_ds,
	grep=cmd_grep,
	run=cmd_run,
	abort=cmd_abort,
	server=cmd_server,
	init=cmd_init,
	urd=cmd_urd,
	curl=cmd_curl,
	method=cmd_method,
	workdir=cmd_workdir,
	board=cmd_board,
	job=cmd_job,
	version=cmd_version,
)

def split_args(argv):
	prev = None
	for ix, arg in enumerate(argv):
		if not arg.startswith('-') and prev != '--config':
			return argv[:ix], argv[ix:]
		prev = arg
	return argv, []

def parse_user_config():
	from accelerator.compat import open
	from os import environ
	cfgdir = environ.get('XDG_CONFIG_HOME')
	if not cfgdir:
		home = environ.get('HOME')
		if not home:
			return None
		cfgdir = join(home, '.config')
	fn = join(cfgdir, 'accelerator', 'config')
	try:
		fh = open(fn, 'r', encoding='utf-8')
	except IOError:
		return None
	with fh:
		from configparser import ConfigParser
		cfg = ConfigParser()
		cfg.optionxform = str # case sensitive (don't downcase aliases)
		cfg.read_file(fh)
		if 'alias' in cfg:
			return cfg['alias']
	return None

def main():
	# As of python 3.8 the default start_method is 'spawn' on macOS.
	# This doesn't work for us. 'fork' is fairly unsafe on macOS,
	# but it's better than not working at all. See
	# https://bugs.python.org/issue33725
	# for more information.
	import multiprocessing
	if hasattr(multiprocessing, 'set_start_method'):
		# If possible, make the forkserver (used by database updates) pre-import everthing
		if hasattr(multiprocessing, 'set_forkserver_preload'):
			multiprocessing.set_forkserver_preload(['accelerator', 'accelerator.server'])
		multiprocessing.set_start_method('fork')

	from accelerator import g
	g.running = 'shell'

	from accelerator.autoflush import AutoFlush
	main_argv, argv = split_args(sys.argv[1:])
	sys.stdout = AutoFlush(sys.stdout)
	sys.stderr = AutoFlush(sys.stderr)

	aliases = {
		'cat': 'grep ""',
	}
	aliases.update(parse_user_config() or ())
	while argv and argv[0] in aliases:
		try:
			expanded = shlex.split(aliases[argv[0]])
		except ValueError as e:
			raise ValueError('Failed to expand alias %s (%r): %s' % (argv[0], aliases[argv[0]], e,))
		more_main_argv, argv = split_args(expanded + argv[1:])
		main_argv.extend(more_main_argv)

	epilog = ['commands:', '']
	cmdlen = max(len(cmd) for cmd in COMMANDS)
	template = '  %%%ds  %%s' % (cmdlen,)
	for cmd, func in sorted(COMMANDS.items()):
		epilog.append(template % (cmd, func.help,))
	epilog.append('')
	epilog.append('aliases:')
	epilog.extend('%s = %s' % item for item in sorted(aliases.items()))
	epilog.append('')
	epilog.append('use %(prog)s <command> --help for <command> usage')
	parser = ArgumentParser(
		usage='%(prog)s [--config CONFIG_FILE] command [args]',
		epilog='\n'.join(epilog),
		formatter_class=RawDescriptionHelpFormatter,
	)
	parser.add_argument('--config', metavar='CONFIG_FILE', help='configuration file')
	parser.add_argument('--version', action='store_true', help='alias for the version command')
	args = parser.parse_args(main_argv)
	if args.version:
		sys.exit(cmd_version(()))
	args.command = argv.pop(0) if argv else None
	if args.command not in COMMANDS:
		parser.print_help(file=sys.stderr)
		print(file=sys.stderr)
		if args.command is not None:
			print('Unknown command "%s"' % (args.command,), file=sys.stderr)
		sys.exit(2)
	config_fn = args.config
	if args.command == 'init':
		config_fn = False
	cmd = COMMANDS[args.command]
	debug_cmd = getattr(cmd, 'is_debug', False)
	try:
		setup(config_fn, debug_cmd)
		argv.insert(0, '%s %s' % (basename(sys.argv[0]), args.command,))
		return cmd(argv)
	except UserError as e:
		print(e, file=sys.stderr)
		return 1
	except IOError as e:
		if e.errno == errno.EPIPE and debug_cmd:
			return
		else:
			raise
