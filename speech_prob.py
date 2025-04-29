from abc import ABC, abstractmethod
from datetime import datetime
from difflib import SequenceMatcher
import re
import pyttsx3

class FestivalBot(ABC):
    @abstractmethod
    def greet(self): pass

    @abstractmethod
    def handle_query(self, query): pass

    @abstractmethod
    def show_schedule(self, day): pass


class TechnovateBot(FestivalBot):
    def __init__(self):
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 160)  # Speaking speed
        self.engine.setProperty('voice', self.engine.getProperty('voices')[2].id)  # Default voice
        
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
        
        # Enhanced command mapping with keywords
        self.__commands = {
            "what is technovate": {
                "func": self.about_technovate,
                "keywords": ["technovate", "about", "festival", "tell me", "explain"]
            },
            "theme for 2025": {
                "func": self.theme,
                "keywords": ["theme", "2025", "this year", "concept", "motto"]
            },
            "team required": {
                "func": self.team_requirement,
                "keywords": ["team", "size", "members", "required", "how many"]
            },
            "technical events": {
                "func": self.tech_events,
                "keywords": ["technical", "tech", "events", "competitions", "hackathon", "coding"]
            },
            "cultural events": {
                "func": self.cultural_events,
                "keywords": ["cultural", "dance", "drama", "music", "performances", "art"]
            },
            "talent show": {
                "func": self.open_stage,
                "keywords": ["open", "mic", "stage", "talent", "show", "perform"]
            },
            "external participants": {
                "func": self.external_participation,
                "keywords": ["external", "outsiders", "allowed", "outside", "college", "other"]
            },
            "how to register": {
                "func": self.registration_info,
                "keywords": ["how", "register", "sign up", "participate", "join", "registration"]
            },
            "register for events": {
                "func": self.event_registration,
                "keywords": ["register", "event", "sign", "participate", "enter"]
            },
            "accommodation": {
                "func": self.accommodation_info,
                "keywords": ["accommodation", "stay", "hostel", "room", "lodging"]
            },
            "food": {
                "func": self.food_info,
                "keywords": ["food", "canteen", "eating", "stalls", "meal"]
            },
            "contact": {
                "func": self.contact_info,
                "keywords": ["contact", "reach", "support", "help", "email", "phone"]
            },
            "last year theme": {
                "func": self.previous_theme,
                "keywords": ["last year", "previous", "theme", "2024", "before"]
            },
            "celebrity guests": {
                "func": self.celeb_guests,
                "keywords": ["celebrities", "guests", "stars", "performers", "famous", "guest"]
            },
            "sponsors": {
                "func": self.past_sponsors,
                "keywords": ["sponsors", "sponsorship", "brands", "supporters","sponsor"]
            },
            "help": {
                "func": self.__help,
                "keywords": ["help", "commands", "what can you do", "options"]
            }
        }

    def speak(self, text):
        """Convert text to speech and print it to console"""
        print(f"Bot: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def greet(self):
        welcome_msg = "🎉 Welcome to Technovate 6.0 Bot! Ask me anything about the event schedule, day-wise or time-wise."
        help_msg = "Type 'help' for suggestions or 'exit' to quit."
        print(f"\n{welcome_msg}\n{help_msg}")
        self.speak(welcome_msg + " " + help_msg)

    def handle_query(self, query):
        query = query.lower().strip()
        
        # First check for day/time queries
        if "day" in query and any(char.isdigit() for char in query):
            self.__handle_day_time_query(query)
            return
            
        # Then check for best matching command
        best_match = self.__find_best_match(query)
        if best_match:
            self.__commands[best_match]["func"]()
        else:
            error_msg = "Hmm, I didn't catch that. Try asking like 'What's on Day 2 at 3 PM?' or type 'help'."
            self.speak(error_msg)

    def __find_best_match(self, query):
        best_score = 0
        best_match = None
        
        for command, data in self.__commands.items():
            # Check direct match first
            if any(keyword in query for keyword in data["keywords"]):
                return command
                
            # Calculate similarity score for each keyword
            for keyword in data["keywords"]:
                ratio = SequenceMatcher(None, query, keyword).ratio()
                if ratio > best_score:
                    best_score = ratio
                    best_match = command
                    
        # Only return if we have a reasonably good match
        return best_match if best_score > 0.6 else None

    def show_schedule(self, day):
        schedule = self.__schedule.get(day, {})
        if not schedule:
            self.speak("Sorry, I don't have events listed for that day.")
            return
        
        schedule_msg = f"Schedule for {day.title()}:"
        print(f"\n📅 {schedule_msg}")
        self.speak(schedule_msg)
        
        for time, event in schedule.items():
            event_msg = f"{time} – {event}"
            print(f"🕒 {event_msg}")
            self.speak(event_msg)

    def __handle_day_time_query(self, query):
        day = ""
        for d in ["day 1", "day 2", "day 3"]:
            if d in query:
                day = d
                break

        time = self.__extract_time(query)

        if not day:
            self.speak("Please mention a valid day (Day 1, Day 2, Day 3).")
            return

        if not time:
            self.speak(f"Here's everything on {day.title()}:")
            self.show_schedule(day)
            return

        event = self.__schedule.get(day, {}).get(time)
        if event:
            event_msg = f"At {time} on {day.title()}, you'll find: {event}"
            print(f"Bot: {event_msg}")
            self.speak(event_msg)
        else:
            self.speak(f"Hmm, no event exactly at {time} on {day.title()}. Here's what we have that day:")
            self.show_schedule(day)

    def __extract_time(self, text):
        text = text.replace("pm", " PM").replace("am", " AM")
        time_patterns = [
            r'(\d{1,2}):(\d{2})\s*PM',
            r'(\d{1,2}):(\d{2})\s*AM',
            r'(\d{1,2})\s*PM',
            r'(\d{1,2})\s*AM'
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, text)
            if match:
                hour = int(match.group(1))
                minute = int(match.group(2)) if len(match.groups()) > 1 else 0
                if "PM" in text and hour != 12:
                    hour += 12
                return f"{hour:02d}:{minute:02d}"
        return None

    def __help(self):
        help_msg = """You can ask me about:
- Event schedules (e.g., 'What's on Day 2 at 4 PM?')
- Festival information (e.g., 'What is Technovate?')
- Registration (e.g., 'How to register for events?')
- Technical/Cultural events
- Accommodation, food, contact info
- Theme, sponsors, celebrity guests

Try asking in your own words!"""
        print(f"\nBot: {help_msg}")
        self.speak(help_msg)

    # ------------------- FAQ Functions -------------------
    def about_technovate(self):
        msg = "Technovate is our college's annual tech-cultural fest, blending technology events with cultural performances over three exciting days!"
        self.speak(msg)

    def theme(self):
        msg = f"This year's theme is \"{self.__theme_2025}\" — celebrating how innovation and collaboration can redefine possibilities!"
        self.speak(msg)

    def team_requirement(self):
        msg = """Team requirements vary by event:
- Technical events: 1-4 members
- Cultural events: Solo or teams up to 8
- Workshops: Individual registration
Check specific event details for exact requirements."""
        self.speak(msg)

    def tech_events(self):
        msg = """Technical events include:
- Hackathon (36-hour coding marathon)
- Coding Speedrun (Network Lab)
- Quiz Runner (Room 121)
- Fiducia (Auditorium)
- And many more exciting competitions!"""
        self.speak(msg)

    def cultural_events(self):
        msg = """Cultural events include:
- Mic Mania (Auditorium)
- Groovify (Auditorium)
- Group Dance (Auditorium)
- Nukkad Natak (Parking Area)
- Artist Night – Seedhe Maut Live Performance"""
        self.speak(msg)

    def open_stage(self):
        msg = """The Talent Show/Open Stage:
- Happens throughout the festival
- 5 minute slots per performer
- Any talent welcome: singing, magic, comedy, etc.
- Sign up at the registration desk"""
        self.speak(msg)

    def external_participation(self):
        msg = """External participants:
- Yes! Students from other colleges can participate
- Need valid college ID for registration
- Some events may have restrictions
- Check with event coordinators for details"""
        self.speak(msg)

    def registration_info(self):
        msg = """How to register:
1. Online: Visit technovate2025.edu/register
2. On-campus: Registration desk near main gate
3. Fees: ₹150 for internal, ₹200 for external
Early bird discounts available!"""
        self.speak(msg)

    def event_registration(self):
        msg = """To register for specific events:
1. First complete general registration
2. Then select events you want to participate in
3. Some events may have additional fees
You can register for multiple events!"""
        self.speak(msg)

    def accommodation_info(self):
        msg = """Accommodation options:
- On-campus hostel: ₹500 per night (limited)
- Partner hotels nearby (discounted rates)
- Need to book in advance through our portal
Contact accommodation@technovate2025.edu for queries"""
        self.speak(msg)

    def food_info(self):
        msg = """Food arrangements:
- Food court with multiple cuisines
- Meal coupons available (₹150 per meal)
- Vegan and special diet options available
- Outside food allowed in designated areas"""
        self.speak(msg)

    def contact_info(self):
        msg = """Contact us at:
- Email: info@technovate2025.edu
- Phone: +91 9876543210
- Social: @Technovate2025 on all platforms
Visit our website for more contact options"""
        self.speak(msg)

    def previous_theme(self):
        msg = """Last year's theme (2024) was:
'Breaking Boundaries: Technology Meets Creativity'"""
        self.speak(msg)

    def celeb_guests(self):
        msg = """Celebrity guests include:
- Artist Night – Seedhe Maut Live Performance
- Special appearances by tech influencers
(Full lineup will be announced soon)"""
        self.speak(msg)

    def past_sponsors(self):
        msg = """Our past sponsors include:
- Tech companies and startups
- Local businesses
- Educational platforms
Interested in sponsoring? Contact sponsor@technovate2025.edu"""
        self.speak(msg)


def run_chatbot():
    bot = TechnovateBot()
    bot.greet()
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            farewell_msg = "Goodbye! Enjoy Technovate 6.0 🌟"
            print(f"Bot: {farewell_msg}")
            bot.speak(farewell_msg)
            break
        bot.handle_query(user_input)


if __name__ == "__main__":
    run_chatbot()
