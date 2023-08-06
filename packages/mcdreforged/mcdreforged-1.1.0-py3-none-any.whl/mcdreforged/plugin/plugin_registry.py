from typing import Dict, List, Callable, Any, TYPE_CHECKING

from mcdreforged.command.builder.command_node import Literal
from mcdreforged.minecraft.rtext import RTextBase
from mcdreforged.plugin.plugin_event import EventListener

if TYPE_CHECKING:
	from mcdreforged.plugin.plugin import AbstractPlugin
	from mcdreforged.plugin.plugin_manager import PluginManager

DEFAULT_LISTENER_PRIORITY = 1000


class HelpMessage:
	def __init__(self, plugin: 'AbstractPlugin', prefix: str, message: str or RTextBase, permission: int):
		self.plugin = plugin
		self.prefix = prefix
		self.message = RTextBase.from_any(message)
		self.permission = permission
		self.__prefix_lower = self.prefix.lower()

	def __lt__(self, other):
		if not isinstance(other, type(self)):
			return False
		if self.__prefix_lower != other.__prefix_lower:
			return self.__prefix_lower < other.__prefix_lower
		return self.prefix < other.prefix

	def __repr__(self):
		return 'HelpMessage[prefix={},message={},permission={}]'.format(self.prefix, self.message, self.permission)


class PluginCommandNode:
	"""
	A Tuple like data class for tracking the plugin of the node
	"""
	def __init__(self, plugin: 'AbstractPlugin', node: Literal):
		self.plugin = plugin
		self.node = node


class PluginRegistry:
	def __init__(self, plugin: 'AbstractPlugin'):
		self.plugin = plugin
		self.event_listeners = {}  # type: Dict[str, List[EventListener]]
		self.help_messages = []
		self.command_roots = []  # type: List[PluginCommandNode]

	def register_help_message(self, help_message: HelpMessage):
		self.help_messages.append(help_message)

	def register_event_listener(self, event_id: str, listener: EventListener):
		listeners = self.event_listeners.get(event_id, [])
		listeners.append(listener)
		self.event_listeners[event_id] = listeners

	def register_command(self, node: Literal):
		if not isinstance(node, Literal):
			raise TypeError('Only Literal node is accepted to be a root node')
		self.command_roots.append(PluginCommandNode(self.plugin, node))

	def clear(self):
		"""
		Invoke this when a plugin gets loaded / reloaded
		:return:
		"""
		self.event_listeners.clear()
		self.help_messages.clear()
		self.command_roots.clear()


class PluginManagerRegistry:
	def __init__(self, plugin_manager: 'PluginManager'):
		self.plugin_manager = plugin_manager
		self.event_listeners = {}  # type: Dict[str, List[EventListener]]
		self.help_messages = []  # type: List[HelpMessage]
		self.command_roots = []  # type: List[PluginCommandNode]

	def clear(self):
		self.event_listeners.clear()
		self.help_messages.clear()
		self.command_roots.clear()

	def collect(self, registry: PluginRegistry):
		for event_id, plg_listeners in registry.event_listeners.items():
			listeners = self.event_listeners.get(event_id, [])
			listeners.extend(plg_listeners)
			self.event_listeners[event_id] = listeners
		self.help_messages.extend(registry.help_messages)
		self.command_roots.extend(registry.command_roots)

	def arrange(self):
		self.help_messages.sort()
		for listeners in self.event_listeners.values():
			listeners.sort()

	def export_commands(self, exporter: Callable[[PluginCommandNode], Any]):
		for node in self.command_roots:
			exporter(node)
