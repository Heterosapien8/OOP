from abc import ABC, abstractmethod
from datetime import datetime
import pyttsx3

# creating the engine for the voice
engine = pyttsx3.init()
engine.setProperty('rate', 160)  # You can adjust the speaking speed
engine.setProperty('voice', engine.getProperty('voices')[0].id)  # Choose the default voice


# ----------------- Abstract Base Class -----------------
class FestivalBot(ABC):
    @abstractmethod
    def greet(self): pass

    @abstractmethod
    def handle_query(self, query): pass

    @abstractmethod
    def show_schedule(self, day): pass


# ----------------- Derived Class: TechnovateBot -----------------
class TechnovateBot(FestivalBot):
    def __init__(self):
        # Encapsulated Data
        self.__schedule = {
            "day 1": {
                "10:30": "Opening Ceremony (Auditorium)",
                "12:00": "Mic Mania (Auditorium)",
                "15:00": "Singing (Auditorium)",
                "16:00": "Nukkad Natak (Parking Area), Hackathon Begins",
                "16:30": "Cricket (Ground near BALCO)",
                "18:00": "Badminton (Sports Complex), Table Tennis (Gym), Volleyball (Court), Basketball (Sports Complex), Football (Football Ground)"
            },
            "day 2": {
                "09:00": "Hackathon Continues",
                "11:00": "Quiz Runner (Room 121)",
                "12:00": "Groovify (Auditorium)",
                "15:00": "Group Dance (Auditorium), ComicCon (Palm Park)",
                "16:30": "Cricket (Ground near BALCO)",
                "18:00": "Badminton (Sports Complex), Table Tennis (Gym), Volleyball (Court), Basketball (Sports Complex), Football (Football Ground)"
            },
            "day 3": {
                "10:00": "Fiducia – Preliminary Round (Auditorium)",
                "11:00": "Coding Speedrun (Network Lab)",
                "12:00": "Fiducia – Final Round (Auditorium)",
                "16:30": "Cricket (Ground near BALCO)",
                "18:00": "Badminton (Sports Complex), Table Tennis (Gym), Volleyball (Court), Basketball (Sports Complex), Football (Football Ground)",
                "20:00": "Artist Night – Seedhe Maut Live Performance"
            }
        }

        self.__theme_2025 = "Innovation and Collaboration Redefined"
        self.__commands = {
            "what is technovate": self.about_technovate,
            "theme for 2025": self.theme,
            "team required": self.team_requirement,
            "technical events": self.tech_events,
            "cultural events": self.cultural_events,
            "talent show": self.open_stage,
            "external participants": self.external_participation,
            "how to register": self.registration_info,
            "register for events": self.event_registration,
            "accommodation": self.accommodation_info,
            "food": self.food_info,
            "contact": self.contact_info,
            "last year theme": self.previous_theme,
            "celebrity guests": self.celeb_guests,
            "sponsors": self.past_sponsors,
            "help": self.__help
        }

    def speak(self, text):
        """Converts the given text to speech."""
        engine.say(text)
        engine.runAndWait()

    def greet(self):
        message = "\n🎉 Welcome to Technovate 6.0 Bot! Ask me anything about the event schedule, day-wise or time-wise. Type 'help' for suggestions or 'exit' to quit."
        print(message)
        self.speak("Welcome to Technovate 6.0 Bot! Ask me anything about the event schedule, day-wise or time-wise. Type help for suggestions or exit to quit.")

    def handle_query(self, query):
        query = query.lower().strip()
        for key in self.__commands:
            if key in query:
                self.__commands[key]()
                return

        if "day" in query and any(char.isdigit() for char in query):
            self.__handle_day_time_query(query)
        else:
            response = "Hmm, I didn't catch that. Try asking like 'What's on Day 2 at 3 PM?' or type 'help'."
            print(f"Bot: {response}")
            self.speak(response)

    def show_schedule(self, day):
        schedule = self.__schedule.get(day, {})
        if not schedule:
            response = "Sorry, I don’t have events listed for that day."
            print(f"Bot: {response}")
            self.speak(response)
            return
        for time, event in schedule.items():
            message = f"🕒 {time} – {event}"
            print(message)
            self.speak(message)

    def __handle_day_time_query(self, query):
        day = ""
        for d in ["day 1", "day 2", "day 3"]:
            if d in query:
                day = d
                break

        time = self.__extract_time(query)

        if not day:
            response = "Please mention a valid day (Day 1, Day 2, Day 3)."
            print(f"Bot: {response}")
            self.speak(response)
            return

        if not time:
            response = f"Here's everything on {day.title()}:"
            print(f"Bot: {response}")
            self.speak(response)
            self.show_schedule(day)
            return

        event = self.__schedule.get(day, {}).get(time)
        if event:
            response = f"At {time} on {day.title()}, you’ll find:\n👉 {event}"
            print(f"Bot: {response}")
            self.speak(response)
        else:
            response = f"Hmm, no event exactly at {time} on {day.title()}. Here's what we have that day:"
            print(f"Bot: {response}")
            self.speak(response)
            self.show_schedule(day)

    def __extract_time(self, text):
        text = text.replace("pm", " PM").replace("am", " AM")
        for word in text.split():
            try:
                return datetime.strptime(word, "%I%p").strftime("%H:00")
            except:
                pass
            try:
                return datetime.strptime(word, "%I:%M%p").strftime("%H:%M")
            except:
                pass
        return None

    def __help(self):
        message = (
            "You can ask me things like:\n"
            "- 'What's happening on Day 2?'\n"
            "- 'Events at 4:30 PM on Day 3?'\n"
            "- 'Schedule for Day 1 at 6 PM'\n"
            "- 'Day 3 full schedule'\n"
            "- 'Theme for 2025?'\n"
            "- 'Technical events?' etc."
        )
        print(f"Bot: {message}")
        self.speak("You can ask me things like: What's happening on Day 2? Events at 4:30 PM on Day 3? Schedule for Day 1 at 6 PM, or Day 3 full schedule.")

    # ------------------- FAQ Functions -------------------
    def about_technovate(self):
        response = "Technovate is our college’s annual tech-cultural fest, blending tech events with cultural performances."
        print(f"Bot: {response}")
        self.speak(response)

    def theme(self):
        response = f"Yes! This year’s theme is \"{self.__theme_2025}\" — celebrating innovation, creativity, and collaboration."
        print(f"Bot: {response}")
        self.speak(response)

    def team_requirement(self):
        print("Bot: Some events are solo, while others need teams of 2–4. Check event pages for details.")

    def tech_events(self):
        print("Bot: We’ve got hackathons, coding contests, robotics challenges, IoT expos, and tech quizzes!")

    def cultural_events(self):
        print("Bot: Dance battles, band performances, fashion shows, open mic nights, and drama competitions await!")

    def open_stage(self):
        print("Bot: Yes! Our Open Mic Stage welcomes singers, poets, and performers. Registrations opening soon!")

    def external_participation(self):
        print("Bot: Yes, many cultural events are open to participants from outside our college. Check event rules.")

    def registration_info(self):
        print("Bot: You can register on our official website under the 'Register' section. Fest passes and event-wise options are available.")

    def event_registration(self):
        print("Bot: Yes, you need to register separately for each event you want to attend.")

    def accommodation_info(self):
        print("Bot: Outstation participants can get hostel accommodation for a nominal charge. Check the 'Stay' section.")

    def food_info(self):
        print("Bot: Yes, food stalls, canteens, and a food court will be active during the fest!")

    def contact_info(self):
        print("Bot: You can talk to this bot or visit the 'Contact Us' page for event coordinators and support.")

    def previous_theme(self):
        print("Bot: Technovate 2024’s theme was ‘Beyond Boundaries’, celebrating limitless innovation and imagination.")

    def celeb_guests(self):
        print("Bot: In past editions, we’ve had Samay Raina and Seedhe Maut perform or speak at the event.")

    def past_sponsors(self):
        print("Bot: Yes! We’ve been sponsored by brands like Jungle Safari in past editions.")


# ----------------- Run the Chatbot -----------------
def run_chatbot():
    bot = TechnovateBot()
    bot.greet()
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            farewell = "Goodbye! Enjoy Technovate 6.0 🌟"
            print(f"Bot: {farewell}")
            bot.speak(farewell)
            break
        bot.handle_query(user_input)




if __name__ == "__main__":
    run_chatbot()