class EventBus:
	def __init__(self):
		self.events = {}

	def subscribe(self, handler, *event_types):
		for etype in event_types:
			self.events.setdefault(etype, []).append(handler)

	def emit(self, event_type, **data):
		if event_type:
			data.update({'event_type': event_type})
			for handler in self.events.get(event_type, ()):
				handler(**data)
