import tkinter as tk
from tkinter import scrolledtext
from abc import ABC, abstractmethod
from datetime import datetime
from difflib import SequenceMatcher
import re
import pyttsx3
import threading

# ========== Your Bot Classes (Original) ==========

class FestivalBot(ABC):
    @abstractmethod
    def greet(self): pass

    @abstractmethod
    def handle_query(self, query): pass

    @abstractmethod
    def show_schedule(self, day): pass

class TechnovateBot(FestivalBot):
    def __init__(self):
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
            "what is technovate": {
                "func": self.about_technovate,
                "keywords": ["what", "technovate", "about", "festival", "tell me", "explain"]
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
                "keywords": ["how", "register", "sign up", "participate", "join"]
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
                "keywords": ["celebrities", "guests", "stars", "performers", "famous"]
            },
            "sponsors": {
                "func": self.past_sponsors,
                "keywords": ["sponsors", "sponsorship", "brands", "supporters"]
            },
            "help": {
                "func": self.__help,
                "keywords": ["help", "commands", "what can you do", "options"]
            }
        }

    def greet(self):
        return "\n Welcome to Technovate 6.0 Bot! Ask me anything about the event schedule, day-wise or time-wise."

    def handle_query(self, query):
        query = query.lower().strip()
        if "day" in query and any(char.isdigit() for char in query):
            return self.__handle_day_time_query(query)
        best_match = self.__find_best_match(query)
        if best_match:
            return self.__commands[best_match]["func"]()
        else:
            return "Bot: Hmm, I didn't catch that. Try asking like 'What's on Day 2 at 3 PM?' or type 'help'."

    def __find_best_match(self, query):
        best_score = 0
        best_match = None
        for command, data in self.__commands.items():
            if any(keyword in query for keyword in data["keywords"]):
                return command
            for keyword in data["keywords"]:
                ratio = SequenceMatcher(None, query, keyword).ratio()
                if ratio > best_score:
                    best_score = ratio
                    best_match = command
        return best_match if best_score > 0.6 else None

    def show_schedule(self, day):
        schedule = self.__schedule.get(day, {})
        if not schedule:
            return "Bot: Sorry, I don't have events listed for that day."
        response = f"\n Schedule for {day.title()}:\n"
        for time, event in schedule.items():
            response += f" {time} – {event}\n"
        return response

    def __handle_day_time_query(self, query):
        day = ""
        for d in ["day 1", "day 2", "day 3"]:
            if d in query:
                day = d
                break
        time = self.__extract_time(query)
        if not day:
            return "Bot: Please mention a valid day (Day 1, Day 2, Day 3)."
        if not time:
            return self.show_schedule(day)
        event = self.__schedule.get(day, {}).get(time)
        if event:
            return f"Bot: At {time} on {day.title()}, you'll find:\n {event}"
        else:
            return f"Bot: Hmm, no event exactly at {time} on {day.title()}. Here's what we have that day:\n" + self.show_schedule(day)

    def __extract_time(self, text):
        text = text.replace("pm", " PM").replace("am", " AM")
        time_patterns = [r'(\d{1,2}):(\d{2})\s*PM', r'(\d{1,2}):(\d{2})\s*AM', r'(\d{1,2})\s*PM', r'(\d{1,2})\s*AM']
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
        return ("\nBot: You can ask me about:\n"
                "- Event schedules (e.g., 'What's on Day 2 at 4 PM?')\n"
                "- Festival information (e.g., 'What is Technovate?')\n"
                "- Registration (e.g., 'How to register for events?')\n"
                "- Technical/Cultural events\n"
                "- Accommodation, food, contact info\n"
                "- Theme, sponsors, celebrity guests\n\n"
                "Try asking in your own words!")

    def about_technovate(self):
        return "Bot: Technovate is our college's annual tech-cultural fest, blending technology events with cultural performances over three exciting days!"

    def theme(self):
        return f"Bot: This year's theme is \"{self.__theme_2025}\" — celebrating how innovation and collaboration can redefine possibilities!"

    def team_requirement(self):
        return ("Bot: Team requirements vary by event:\n"
                "- Technical events: 1-4 members\n"
                "- Cultural events: Solo or teams up to 8\n"
                "- Workshops: Individual registration\n"
                "Check specific event details for exact requirements.")

    def tech_events(self):
        return ("Bot: Technical events include:\n"
                "- Hackathon (36-hour coding marathon)\n"
                "- Coding Speedrun (Network Lab)\n"
                "- Quiz Runner (Room 121)\n"
                "- Fiducia (Auditorium)\n"
                "- And many more exciting competitions!")

    def cultural_events(self):
        return ("Bot: Cultural events include:\n"
                "- Mic Mania (Auditorium)\n"
                "- Groovify (Auditorium)\n"
                "- Group Dance (Auditorium)\n"
                "- Nukkad Natak (Parking Area)\n"
                "- Artist Night – Seedhe Maut Live Performance")

    def open_stage(self):
        return ("Bot: The Talent Show/Open Stage:\n"
                "- Happens throughout the festival\n"
                "- 5 minute slots per performer\n"
                "- Any talent welcome: singing, magic, comedy, etc.\n"
                "- Sign up at the registration desk")

    def external_participation(self):
        return ("Bot: External participants:\n"
                "- Yes! Students from other colleges can participate\n"
                "- Need valid college ID for registration\n"
                "- Some events may have restrictions\n"
                "- Check with event coordinators for details")

    def registration_info(self):
        return ("Bot: How to register:\n"
                "1. Online: Visit technovate2025.edu/register\n"
                "2. On-campus: Registration desk near main gate\n"
                "3. Fees: ₹150 for internal, ₹200 for external\n"
                "Early bird discounts available!")

    def event_registration(self):
        return ("Bot: To register for specific events:\n"
                "1. First complete general registration\n"
                "2. Then select events you want to participate in\n"
                "3. Some events may have additional fees\n"
                "You can register for multiple events!")

    def accommodation_info(self):
        return ("Bot: Accommodation options:\n"
                "- On-campus hostel: ₹500 per night (limited)\n"
                "- Partner hotels nearby (discounted rates)\n"
                "- Need to book in advance through our portal\n"
                "Contact accommodation@technovate2025.edu for queries")

    def food_info(self):
        return ("Bot: Food arrangements:\n"
                "- Food court with multiple cuisines\n"
                "- Meal coupons available (₹150 per meal)\n"
                "- Vegan and special diet options available\n"
                "- Outside food allowed in designated areas")

    def contact_info(self):
        return ("Bot: Contact us at:\n"
                "- Email: info@technovate2025.edu\n"
                "- Phone: +91 9876543210\n"
                "- Social: @Technovate2025 on all platforms\n"
                "Visit our website for more contact options")

    def previous_theme(self):
        return "Bot: Last year's theme (2024) was: 'Breaking Boundaries: Technology Meets Creativity'"

    def celeb_guests(self):
        return ("Bot: Celebrity guests include:\n"
                "- Artist Night – Seedhe Maut Live Performance\n"
                "- Special appearances by tech influencers\n"
                "(Full lineup will be announced soon)")

    def past_sponsors(self):
        return ("Bot: Our past sponsors include:\n"
                "- Tech companies and startups\n"
                "- Local businesses\n"
                "- Educational platforms\n"
                "Interested in sponsoring? Contact sponsor@technovate2025.edu")

# ========== GUI Code (with speaking) ==========

engine = pyttsx3.init()
engine.setProperty('rate', 160)

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def run_gui():
    bot = TechnovateBot()

    root = tk.Tk()
    root.title("Technovate 6.0 Bot")

    chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Helvetica", 12))
    chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    chat_area.config(state='disabled')

    user_input = tk.Entry(root, font=("Helvetica", 12))
    user_input.pack(padx=10, pady=(0,10), fill=tk.X)

    def send_message(event=None):
        message = user_input.get().strip()
        if not message:
            return

        chat_area.config(state='normal')
        chat_area.insert(tk.END, f"\nYou: {message}\n", "user")
        chat_area.tag_config("user", justify='right')

        if message.lower() in ["exit", "quit", "bye"]:
            response = "Bot: Goodbye! Enjoy Technovate 6.0 and see you next time!"
            chat_area.insert(tk.END, f"{response}\n", "bot")
            chat_area.tag_config("bot", justify='left')
            threading.Thread(target=speak_text, args=(response,)).start()
            root.after(1000, root.destroy)
            return

        response = bot.handle_query(message)
        chat_area.insert(tk.END, f"{response}\n", "bot")
        chat_area.tag_config("bot", justify='left')

        threading.Thread(target=speak_text, args=(response,)).start()

        user_input.delete(0, tk.END)
        chat_area.config(state='disabled')
        chat_area.yview(tk.END)

    user_input.bind("<Return>", send_message)

    chat_area.config(state='normal')
    greeting = bot.greet()
    chat_area.insert(tk.END, greeting + "\n", "bot")
    chat_area.tag_config("bot", justify='left')
    chat_area.config(state='disabled')

    threading.Thread(target=speak_text, args=(greeting,)).start()

    root.mainloop()

if __name__ == "__main__":
    run_gui()
