
class ProtocalError(Exception):
	def __init__(self, message="Unknown or Unsupported protocol."):
		self.message = message
		super().__init__(self.message)

class ConfigError(Exception):
	def __init__(self, message="Unexpected configuration error."):
		self.message = message
		super().__init__(self.message)