import os
import re

# Define the Todo class
class Todo:
    def __init__(self, description, complete):
        self.description = description # a string
        self.complete = complete # a boolean

    def __str__(self):
        return f"{self.description} ({'Done' if self.complete else 'Pending'})"

# # Define the TimelineEntry class
# class TimelineEntry:
#     def __init__(self, header, entry):
#         self.header = header # a string
#         self.entry = entry # a string

#     def __str__(self):
#         return f"{self.header}: {self.entry}"

# Define the JournalEntry class
class JournalEntry:
    def __init__(self, date, morning, coffee_log, today, timeline, night):
        self.date = date # a string
        self.morning = morning # a string
        self.coffee_log = coffee_log # a list of strings
        self.today = today # a list of Todo objects
        self.timeline = timeline # a list of TimelineEntry objects
        self.night = night # a string

    @classmethod
    def from_file(cls, filename):
        # Read the file and parse the data
        with open(filename) as f:
            lines = f.readlines()
            date = "" # the date string
            morning = "" # the morning string
            coffee_log = [] # the coffee log list
            today = [] # the today list
            timeline = [] # the timeline list
            night = "" # the night string
            mode = "" # keep track of the current section
            for line in lines:
                line = line.strip()
                if line.startswith("<div"):
                    # Parse a header and set the mode accordingly
                    if "journal-h1" in line:
                        mode = "date"
                        # print("Date detected")
                    elif "🌄 gm" in line:
                        mode = "morning"
                        # print("gm detected")
                    elif "🍵 log" in line:
                        mode = "coffee_log"
                        # print("🍵 log detected")
                    elif "🔥 Today" in line:
                        mode = "today"
                        # print("🔥 Today detected")
                    elif "📃 Timeline" in line:
                        mode = "timeline"
                        # print("📃 Timeline detected")
                    elif "🌠 gn" in line:
                        mode = "night"
                        # print("🌠 gn detected")
                else:
                    # Parse the content according to the mode
                    if mode == "date":
                        date = line
                    elif mode == "morning":
                        morning = line
                    elif mode == "coffee_log":
                        coffee_log.append(line)
                    elif mode == "today":
                        match = re.match (r"^\s*-\s*(?:\[([x ])\]\s*)?(?:(?:<mark[^>]*>)?([\u263a-\U0001f645]+)(?:<\/mark>)?|(\d{1,2}:\d{2}))?(?:\s*(?:<mark[^>]*>)?([\u263a-\U0001f645]+)(?:<\/mark>)?|(\d{1,2}:\d{2}))?\s*(.+)$", line)
                        # Group 1: checked (status) value, if the x is present
                        # Group 2: emojis before or after the time, if any
                        # Group 3: time before or after the emojis, if any
                        # Group 4: emojis before or after the time, if any
                        # Group 5: time before or after the emojis, if any
                        # Group 6: description
                        if match:
                            status = match.group(1)
                            emojis = match.group(2) or match.group(4)
                            time = match.group(3) or match.group(5)
                            description = match.group(6).strip()
                            complete = status == "x"
                            todo = Todo(description, complete)
                            # print("added todo: {}".format(todo))
                            today.append(todo)
                    elif mode == "timeline":
                        # # Parse a timeline entry
                        # parts = line.split(":")
                        # header = parts[0].strip()
                        # entry = parts[1].strip()
                        # timeline_entry = TimelineEntry(header, entry)
                        timeline.append(line)
                    elif mode == "night":
                        night = line

        # Create and return a JournalEntry object
        return cls(date, morning, coffee_log, today, timeline, night)

    def __str__(self):
        # Format the data as a string
        result = f"{self.date}\n{self.morning}\n{','.join(self.coffee_log)}\n"
        for todo in self.today:
            result += f"{todo}\n"
        result += "Timeline\n"
        for timeline_entry in self.timeline:
            result += f"{timeline_entry}\n"
        result += f"Night\n{self.night}"
        return result

# Define the Journal class
class Journal:
    def __init__(self):
        self.entries = [] # a list of JournalEntry objects

    def add_entry(self, entry):
        # Add a JournalEntry object to the list
        self.entries.append(entry)

    def get_entry_by_date(self, date):
        # date is a string in the format "21_Friday"
        for entry in self.entries:
            if entry.date == date:
                return entry
        return None
    
    def get_incomplete_todos(self):
        incomplete_todos = [] # A list of incomplete Todo objects
        print('Getting incomplete todos. {} entries loaded'.format(len(self.entries)))
        for entry in self.entries:
            # print(entry)
            for todo in entry.today:
                # print(todo)
                if not todo.complete: # If the todo is not complete
                    incomplete_todos.append(todo) # Add it to the list
        return incomplete_todos # Return the list of incomplete todos

    @classmethod
    def from_directory(cls, directory):
        print('Loading from directory {}'.format(directory))

        journal = cls()

        # Compile the regex
        pattern = re.compile(r'.*([1-2][0-9]{3})/(0[1-9]|1[0-2])-(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)/([0-2][0-9]|3[0-1])_(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\.md')

        # Iterate over the files in the path
        for root, dirs, files in os.walk(directory):
            for file in files:
                full_path = os.path.join(root, file)
                # print(full_path)
                # Check if the file matches the regex
                if pattern.match(full_path):
                    # Print the file name
                    # print(file)
                    filepath = os.path.join(root, file) # get the full path of the file
                    # print("Loading {}".format(filepath))
                    entry = JournalEntry.from_file(filepath)
                    journal.add_entry(entry)
        
        # Return a Journal object
        return journal

    def __str__(self):
        # Format the data as a string
        result = ""
        for entry in self.entries:
            result += f"{entry}\n\n"
        
        return result