class Layout:
    def __init__(self):
        self.widgets = []

    def add(self, widget):
        self.widgets.append(widget)

    def handle_events(self, events):
        for event in events:
            for widget in self.widgets:
                if widget.enabled:
                    widget.handle_event(event)

    def update(self, dt):
        for widget in self.widgets:
            if widget.visible:
                widget.update(dt)

    def draw(self, screen):
        for widget in self.widgets:
            if widget.visible:
                widget.draw(screen)