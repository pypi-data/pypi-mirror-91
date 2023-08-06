from awehflow.events.base import EventHandler


class AlertsEventHandler(EventHandler):
    def __init__(self, alerters, alert_on):
        self.alerters = alerters
        self.alert_on = alert_on

    def catch_all(self, event):
        if event.get('name') in self.alert_on:
            for alerter in self.alerters:
                alerter.alert(event)
