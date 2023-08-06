"""
The place to reacting information from the server
"""
import queue
import time
from typing import TYPE_CHECKING

from mcdreforged import constant
from mcdreforged.info import Info, InfoSource
from mcdreforged.reactor.impl.general_reactor import GeneralReactor
from mcdreforged.reactor.impl.player_reactor import PlayerReactor
from mcdreforged.reactor.impl.server_reactor import ServerReactor
from mcdreforged.utils.logger import ServerLogger, DebugOption

if TYPE_CHECKING:
	from mcdreforged import MCDReforgedServer


class InfoReactorManager:
	def __init__(self, mcdr_server: 'MCDReforgedServer'):
		self.mcdr_server = mcdr_server
		self.last_queue_full_warn_time = None
		self.server_logger = ServerLogger('Server')
		self.reactors = []

	def load_reactors(self):
		self.reactors.clear()
		self.reactors.extend([
			GeneralReactor(self.mcdr_server),
			PlayerReactor(self.mcdr_server),
			ServerReactor(self.mcdr_server),
		])
		# TODO custom reactors

	def process_info(self, info: Info):
		for reactor in self.reactors:
			try:
				reactor.react(info)
			except:
				self.mcdr_server.logger.exception(self.mcdr_server.tr('info_reactor_manager.react.error', type(reactor).__name__))  # TODO: fix translation
		self.__post_process_info(info)

	def __post_process_info(self, info: Info):
		if info.source == InfoSource.SERVER and info.should_echo():
			self.server_logger.info(info.raw_content)

		if info.source == InfoSource.CONSOLE and info.should_send_to_server():
			self.mcdr_server.send(info.content)  # send input command to server's stdin

	def put_info(self, info):
		info.attach_mcdr_server(self.mcdr_server)
		try:
			self.mcdr_server.task_executor.add_info_task(lambda: self.process_info(info), info.is_user)
		except queue.Full:
			current_time = time.time()
			logging_method = self.mcdr_server.logger.debug
			kwargs = {'option': DebugOption.REACTOR}
			if self.last_queue_full_warn_time is None or current_time - self.last_queue_full_warn_time >= constant.REACTOR_QUEUE_FULL_WARN_INTERVAL_SEC:
				logging_method = self.mcdr_server.logger.warning
				kwargs = {}
				self.last_queue_full_warn_time = current_time
			logging_method(self.mcdr_server.tr('info_reactor_manager.info_queue.full'), **kwargs)
