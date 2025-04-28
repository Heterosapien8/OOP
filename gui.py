import tkinter as tk
from tkinter import scrolledtext, Menu
from abc import ABC, abstractmethod
from datetime import datetime
import pyttsx3
import threading
import time

# Setting up the voice engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('voice', engine.getProperty('voices')[0].id)

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
        self.__schedule = {
            "day 1": {
                "10:30": "🎤 Opening Ceremony (Auditorium)",
                "12:00": "🎤 Mic Mania (Auditorium)",
                "15:00": "🎶 Singing (Auditorium)",
                "16:00": "🎭 Nukkad Natak (Parking Area), 💻 Hackathon Begins",
                "16:30": "🏏 Cricket (Ground near BALCO)",
                "18:00": "🏸 Badminton (Sports Complex), 🏓 Table Tennis (Gym), 🏐 Volleyball (Court), 🏀 Basketball (Sports Complex), ⚽ Football (Football Ground)"
            },
            "day 2": {
                "09:00": "💻 Hackathon Continues",
                "11:00": "🧠 Quiz Runner (Room 121)",
                "12:00": "💃 Groovify (Auditorium)",
                "15:00": "💃 Group Dance (Auditorium), 🎭 ComicCon (Palm Park)",
                "16:30": "🏏 Cricket (Ground near BALCO)",
                "18:00": "🏸 Badminton (Sports Complex), 🏓 Table Tennis (Gym), 🏐 Volleyball (Court), 🏀 Basketball (Sports Complex), ⚽ Football (Football Ground)"
            },
            "day 3": {
                "10:00": "🤝 Fiducia – Preliminary Round (Auditorium)",
                "11:00": "👨‍💻 Coding Speedrun (Network Lab)",
                "12:00": "🤝 Fiducia – Final Round (Auditorium)",
                "16:30": "🏏 Cricket (Ground near BALCO)",
                "18:00": "🏸 Badminton (Sports Complex), 🏓 Table Tennis (Gym), 🏐 Volleyball (Court), 🏀 Basketball (Sports Complex), ⚽ Football (Football Ground)",
                "20:00": "🎤 Artist Night – Seedhe Maut Live Performance"
            }
        }

        self.__theme_2025 = "🌟 Innovation and Collaboration Redefined 🌟"
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
        self.response = ""

    def speak(self, text):
        threading.Thread(target=self.__speak_thread, args=(text,)).start()

    def __speak_thread(self, text):
        engine.say(text)
        engine.runAndWait()

    def greet(self):
        self.response = "🎉 Welcome to Technovate 6.0 Bot! Type 'help' for suggestions or 'exit' to quit."
        self.speak(self.response)
        return self.response

    def handle_query(self, query):
        query = query.lower().strip()
        for key in self.__commands:
            if key in query:
                self.__commands[key]()
                return self.response

        if "day" in query and any(char.isdigit() for char in query):
            return self.__handle_day_time_query(query)
        else:
            self.response = "🤔 I didn't catch that. Try 'events on Day 2 at 3 PM' or type 'help'."
            self.speak(self.response)
            return self.response

    def show_schedule(self, day):
        schedule = self.__schedule.get(day, {})
        if not schedule:
            self.response = "😔 Sorry, no events listed for that day."
            self.speak(self.response)
            return self.response
        output = []
        for time, event in schedule.items():
            output.append(f"🕒 {time} – {event}")
        self.response = "\n".join(output)
        self.speak(self.response)
        return self.response

    def __handle_day_time_query(self, query):
        day = ""
        for d in ["day 1", "day 2", "day 3"]:
            if d in query:
                day = d
                break

        time = self.__extract_time(query)

        if not day:
            self.response = "❗ Please mention a valid day (Day 1, Day 2, Day 3)."
            self.speak(self.response)
            return self.response

        if not time:
            self.response = f"📅 Here's everything on {day.title()}:\n" + self.show_schedule(day)
            return self.response

        event = self.__schedule.get(day, {}).get(time)
        if event:
            self.response = f"📍 At {time} on {day.title()}, you’ll find:\n👉 {event}"
        else:
            self.response = f"😅 No event exactly at {time} on {day.title()}. Here's the full day schedule:\n" + self.show_schedule(day)
        self.speak(self.response)
        return self.response

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
        self.response = (
            "💬 You can ask me things like:\n"
            "- 'What's happening on Day 2?'\n"
            "- 'Events at 4:30 PM on Day 3?'\n"
            "- 'Theme for 2025?'\n"
            "- 'Technical events?'\n"
            "- 'How to register?'"
        )
        self.speak(self.response)

    # FAQ functions
    def about_technovate(self): self.__set_response("🎉 Technovate is the annual tech-cultural fest of our college!")
    def theme(self): self.__set_response(f"🎨 This year’s theme is \"{self.__theme_2025}\".")
    def team_requirement(self): self.__set_response("👥 Some events are solo, others are team events (2–4 members).")
    def tech_events(self): self.__set_response("🛠️ Hackathons, coding contests, robotics, quizzes await you!")
    def cultural_events(self): self.__set_response("🎭 Dance battles, music shows, drama, fashion shows!")
    def open_stage(self): self.__set_response("🎤 Yes, open mic for singers, poets, performers is available!")
    def external_participation(self): self.__set_response("🌐 External participants are allowed in several events.")
    def registration_info(self): self.__set_response("📝 Register via our official Technovate website!")
    def event_registration(self): self.__set_response("📝 Each event has its own registration link.")
    def accommodation_info(self): self.__set_response("🏠 Hostels available for outstation participants.")
    def food_info(self): self.__set_response("🍕 Food stalls, canteens, and a food court available!")
    def contact_info(self): self.__set_response("📞 Visit 'Contact Us' page for coordinator contacts.")
    def previous_theme(self): self.__set_response("🛤️ 2024’s theme was ‘Beyond Boundaries’.")
    def celeb_guests(self): self.__set_response("🌟 Past guests: Samay Raina, Seedhe Maut!")
    def past_sponsors(self): self.__set_response("🏆 Jungle Safari was a proud sponsor!")

    def __set_response(self, text):
        self.response = text
        self.speak(text)

# ----------------- GUI Application -----------------
class ChatGUI:
    def __init__(self, root):
        self.bot = TechnovateBot()
        self.root = root
        self.root.title("Technovate 6.0 Chatbot")
        self.root.geometry("600x700")

        # 🛠️ Create widgets first
        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', font=("Arial", 12))
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(root, font=("Arial", 14))
        self.entry.pack(padx=10, pady=10, fill=tk.X)
        self.entry.bind("<Return>", self.send_message)

        # Menu
        menu = Menu(root)
        root.config(menu=menu)
        view_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Light Mode", command=self.light_mode)
        view_menu.add_command(label="Dark Mode", command=self.dark_mode)

        # 🎨 Set theme now
        self.light_mode()

        self.display_message("Technovate Bot", self.bot.greet())

    def light_mode(self):
        self.root.configure(bg="#f1f1f1")
        self.chat_area.configure(bg="white", fg="black")
        self.entry.configure(bg="white", fg="black")

    def dark_mode(self):
        self.root.configure(bg="#2c2f33")
        self.chat_area.configure(bg="#23272a", fg="white")
        self.entry.configure(bg="#2c2f33", fg="white")

    def display_message(self, sender, message, side="left"):
        self.chat_area.config(state='normal')
        if side == "left":
            self.chat_area.insert(tk.END, f"\n{sender}: {message}\n", "left")
        else:
            self.chat_area.insert(tk.END, f"\nYou: {message}\n", "right")
        self.chat_area.tag_configure("left", justify='left', foreground="blue")
        self.chat_area.tag_configure("right", justify='right', foreground="green")
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

    def send_message(self, event=None):
        user_msg = self.entry.get()
        if not user_msg.strip():
            return
        self.display_message("You", user_msg, side="right")
        self.entry.delete(0, tk.END)

        if user_msg.lower() in ["exit", "quit", "bye"]:
            self.display_message("Technovate Bot", "👋 Goodbye! Enjoy Technovate 6.0!", side="left")
            self.root.after(2000, self.root.destroy)
            return

        threading.Thread(target=self.bot_reply, args=(user_msg,)).start()

    def bot_reply(self, user_msg):
        time.sleep(0.5)
        self.display_message("Technovate Bot", "💬 Typing...", side="left")
        time.sleep(1)
        self.chat_area.config(state='normal')
        self.chat_area.delete("end-2l", "end-1l")
        self.chat_area.config(state='disabled')

        bot_response = self.bot.handle_query(user_msg)
        self.display_message("Technovate Bot", bot_response, side="left")

# ----------------- Run the Application -----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatGUI(root)
    root.mainloop()
