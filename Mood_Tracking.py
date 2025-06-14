
"""
Objective: Create a console-based personal mood journal app where the user can log daily 
thoughts and the app analyzes their mood trend using simple logic. Helps beginners practice
real-life Python skills.
"""

# Project: 🌟 Mood Journal & Sentiment Tracker

import datetime
import json
from collections import Counter

# Create a User Profile (Class)
class Diarist:
    def __init__(self, name):
        self.name = name
        self.entries = []

    def add_entry(self, text, mood):
        entry = {
            "date": datetime.date.today().isoformat(),
            "text": text,
            "mood": mood
        }
        self.entries.append(entry)

    def show_history(self):
        if not self.entries:
            print("No mood history found.")
            return
        print("\n📜 Mood History:")
        for entry in self.entries:
            print(f"{entry['date']}: {entry['mood']} - {entry['text']}")

    def most_common_mood(self):
        if not self.entries:
            print("No mood data available.")
            return
        moods = [entry["mood"] for entry in self.entries]
        mood, count = Counter(moods).most_common(1)[0]
        print(f"Most common mood: {mood} ({count} times)")

    def file_name(self):
        return f"{self.name}_journal.json"

    def save(self):
        try:
            with open(self.file_name(), "w", encoding="utf-8") as f:
                json.dump(self.entries, f, indent=4)
            print("✅ Journal saved successfully.")
        except Exception as e:
            print("❌ Error saving file:", e)

    def load(self):
        try:
            with open(self.file_name(), "r", encoding="utf-8") as f:
                self.entries = json.load(f)
            print("📂 Previous journal loaded.")
        except FileNotFoundError:
            self.entries = []
        except Exception as e:
            print("❌ Error loading journal:", e)
            self.entries = []

# Mood Analyzer Function

def mood_analyzer(text):
    text = text.lower()
    happy = ["happy", "great", "love", "optimism", "excited", "pride", "cool"]
    sad = ["sad", "tired", "angry", "upset", "bored", "depressed", "anxious"]
    neutral = ["okay", "fine", "normal", "average", "calm", "meh"]

    score = {"Happy": 0, "Sad": 0, "Neutral": 0}
    for word in text.split():
        if word in happy:
            score["Happy"] += 1
        elif word in sad:
            score["Sad"] += 1
        elif word in neutral:
            score["Neutral"] += 1

    return max(score, key=score.get) if max(score.values()) > 0 else "Unknown"

# Bonus Feature: Suggest Activity Based on Mood

def recommend_activity(mood):
    suggestions = {
        "Happy": "Celebrate, savoring the moment, and let the good vibes flow. ✨",
        "Sad": "1. Walk under moonlight. 2. order Pizza. 3. eat chocolates 💛",
        "Neutral": "Read a good book or enjoy a warm drink. ☕",
        "Unknown": "Try expressing more or journaling deeply. ✍️"
    }
    return suggestions.get(mood, "Take care of yourself 💖")

# Bonus: Weekly Mood Summary

def weekly_summary(entries):
    today = datetime.date.today()
    last_7_days = [
        j for j in entries
        if (today - datetime.date.fromisoformat(j['date'])).days < 7
    ]
    if not last_7_days:
        print("No entries in the past 7 days.")
        return
    mood_counts = Counter(j["mood"] for j in last_7_days)
    print("\n📅 Weekly Mood Summary:")
    for mood, count in mood_counts.items():
        print(f"{mood}: {count} time(s)")

# Bonus: Export to .txt File

def export_to_txt(entries, name):
    filename = f"{name}_journal_export.txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for e in entries:
                f.write(f"{e['date']} - {e['mood']} - {e['text']}\n")
        print(f"📁 Journal exported to '{filename}'")
    except Exception as e:
        print("❌ Error exporting to text file:", e)

# 🚀 Main Application

def run_journal():
    name = input("Enter your name: ").strip()
    if not name:
        print("⚠️ Name cannot be empty.")
        return

    user = Diarist(name)
    user.load()

    while True:
        print("\n--- Mood Journal Menu ---")
        print("1. Add Entry")
        print("2. Show Mood History")
        print("3. Show Most Common Mood")
        print("4. Recommend Activity")
        print("5. Weekly Mood Summary")
        print("6. Export to .txt")
        print("7. Save & Exit")

        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            text = input("How do you feel today? ✍️\n").strip()
            if not text:
                print("⚠️ Entry cannot be empty.")
                continue
            mood = mood_analyzer(text)
            print(f"Detected Mood: {mood}")
            print(recommend_activity(mood))
            user.add_entry(text, mood)

        elif choice == "2":
            user.show_history()

        elif choice == "3":
            user.most_common_mood()

        elif choice == "4":
            if user.entries:
                mood = user.entries[-1]["mood"]
                print(recommend_activity(mood))
            else:
                print("⚠️ No entries to analyze mood from.")

        elif choice == "5":
            weekly_summary(user.entries)

        elif choice == "6":
            export_to_txt(user.entries, user.name)

        elif choice == "7":
            user.save()
            print("👋 Goodbye and take care!")
            break

        else:
            print("❌ Invalid choice. Try again.")

# Run the app
if __name__ == "__main__":
    run_journal()
