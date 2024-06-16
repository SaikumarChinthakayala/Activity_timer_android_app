import csv
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

class TimerApp(App):
    def build(self):
        self.event_type = None
        self.in_time = None

        root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title Label
        self.label = Label(text="Select an event to start timing",
                           font_size='24sp',
                           size_hint_y=None,
                           height=50,
                           color=(0.2, 0.6, 0.8, 1))
        root.add_widget(self.label)

        # Event Buttons Layout
        button_layout = GridLayout(cols=3, size_hint_y=None, height=60, spacing=10)
        
        for event in ["Call", "Bathroom", "Office"]:
            btn = Button(text=event, font_size='20sp', background_color=(0.2, 0.6, 0.8, 1), color=(1, 1, 1, 1))
            btn.bind(on_press=self.select_event)
            button_layout.add_widget(btn)
        
        root.add_widget(button_layout)

        # IN and OUT Buttons Layout
        self.in_out_layout = GridLayout(cols=2, size_hint_y=None, height=60, spacing=10)
        self.in_button = Button(text='IN', font_size='20sp', background_color=(0.2, 0.8, 0.2, 1), color=(1, 1, 1, 1))
        self.in_button.bind(on_press=self.mark_in_time)
        self.out_button = Button(text='OUT', font_size='20sp', background_color=(0.8, 0.2, 0.2, 1), color=(1, 1, 1, 1))
        self.out_button.bind(on_press=self.mark_out_time)

        self.in_out_layout.add_widget(self.in_button)
        self.in_out_layout.add_widget(self.out_button)
        root.add_widget(self.in_out_layout)

        return root

    def select_event(self, instance):
        self.event_type = instance.text
        self.label.text = f"Selected event: {self.event_type}"

    def mark_in_time(self, instance):
        if self.event_type:
            self.in_time = datetime.now()
            self.label.text = f"{self.event_type} IN time marked at {self.in_time.strftime('%H:%M:%S')}"

    def mark_out_time(self, instance):
        if self.event_type and self.in_time:
            out_time = datetime.now()
            self.save_to_csv(self.event_type, self.in_time, out_time)
            self.label.text = f"{self.event_type} OUT time marked at {out_time.strftime('%H:%M:%S')}"
            self.in_time = None

    def save_to_csv(self, event_type, in_time, out_time):
        filename = f"{event_type.lower()}.csv"
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().date(), in_time.time(), out_time.time()])

if __name__ == '__main__':
    TimerApp().run()
