import csv
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class TimerApp(App):
    def build(self):
        self.event_type = None
        self.in_time = None

        layout = BoxLayout(orientation='vertical')

        self.label = Label(text="Select an event to start timing")
        layout.add_widget(self.label)

        button_layout = BoxLayout(size_hint_y=None, height='50dp')
        
        for event in ["Call", "Bathroom", "Office"]:
            btn = Button(text=event)
            btn.bind(on_press=self.select_event)
            button_layout.add_widget(btn)
        
        layout.add_widget(button_layout)

        self.in_out_layout = BoxLayout(size_hint_y=None, height='50dp')
        self.in_button = Button(text='IN')
        self.in_button.bind(on_press=self.mark_in_time)
        self.out_button = Button(text='OUT')
        self.out_button.bind(on_press=self.mark_out_time)

        self.in_out_layout.add_widget(self.in_button)
        self.in_out_layout.add_widget(self.out_button)
        layout.add_widget(self.in_out_layout)

        return layout

    def select_event(self, instance):
        self.event_type = instance.text
        self.label.text = f"Selected event: {self.event_type}"

    def mark_in_time(self, instance):
        if self.event_type:
            self.in_time = datetime.now()
            self.label.text = f"{self.event_type} IN time marked at {self.in_time}"

    def mark_out_time(self, instance):
        if self.event_type and self.in_time:
            out_time = datetime.now()
            self.save_to_csv(self.event_type, self.in_time, out_time)
            self.label.text = f"{self.event_type} OUT time marked at {out_time}"
            self.in_time = None

    def save_to_csv(self, event_type, in_time, out_time):
        filename = f"{event_type.lower()}.csv"
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().date(), in_time.time(), out_time.time()])

if __name__ == '__main__':
    TimerApp().run()
