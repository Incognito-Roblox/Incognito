class EventManager:
    listeners = {}

    @staticmethod
    def subscribe(event_type, listener):
        if event_type not in EventManager.listeners:
            EventManager.listeners[event_type] = []
        EventManager.listeners[event_type].append(listener)

    @staticmethod
    def emit(event_type, data):
        for listener in EventManager.listeners.get(event_type, []):
            listener(data)