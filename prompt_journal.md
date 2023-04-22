# Bing prompts to get my journal automation in place

## Creating the classes to store my journal

Create the python classes and all necessary functions and classmethods for the following. Journal class stores a collection of another class, JournalEntry. JournalEntry is a single file named {DATE} where date is the day as 21_Friday.md and in this file it has a date, a "morning" string, a "coffee log" array of strings, a "today" array of Todo class objects (a string description with a boolean on complete), a timeline array of TimelineEntries (a header string and a entry string), and a "night" string. These classes will be used to read in a file to load in all the data, it will not be used to write to a file.

> Looked mostly right but parsing the file was awful so it needed more instruction there

Update the from_file method so that the file is analyzed more dynamically by checking for the presence of a header, after which all the text will be that section until the next header. My headers are defined as html inside of the markdown, like this: <div class="standard-header journal-h1 default">Tuesday, April 18th</div> <div class="standard-header journal-h2 default">🌄 gm</div> Slept in, guess I have been stressed lately. <div class="standard-header journal-h2 default">🍵 log</div> * 1 cup caf at 10 <div class="standard-header journal-h2 default">🔥 Today</div> - [x] Morning Where the date is inside the first header, the morning section is after 🌄 gm but before the next div block, 🍵 log is the coffee section, 🔥 Today is the today section with each line there being a Todo, etc

> The way it solved it using modes was cool. I understand it and can take it from here

## Trying to get the API side of things set up for me next

Okay assume that I already asked an AI to do this: { Create the python classes and all necessary functions and classmethods for the following. Journal class stores a collection of another class, JournalEntry. JournalEntry is a single file named {DATE} where date is the day as 21_Friday.md and in this file it has a date, a "morning" string, a "coffee log" array of strings, a "today" array of Todo class objects (a string description with a boolean on complete), a timeline array of TimelineEntries (a header string and a entry string), and a "night" string. These classes will be used to read in a file to load in all the data, it will not be used to write to a file. } and it created the classes I needed. Now assume I have a flask API already implemented. Create just the additions to the Flask api where on starting the API it will scan folders of folders of my journal, arranged in {YEAR}/{MONTH}/{DAY} and load all the JournalEntries into a Journal. Then add an endpoint that analyzes the Journal for all occurances where the Todo objects contain incomplete items.

> Gave me Journal implementations but with useful edition using get_incomplete_todos, and a good scan_and_load method for finding journal files

> I lost the page and had to re-ask it again. The next time I pasted this, it created an image of code??? Then I asked a third time and it gave me a good answer again, this time including a get_entry_by_date which I found useful. I also blew my mind with @app.before_first_request - def load_journal():!!!

> I tried to use its code for its route but it didnt work and I wanted the Journal(Resource) method of doing it

## Get it to create a Resource class

Instead of using app.route, use Journal(Resource) and define it with a get()

In flask you can define Resource classes, such as this: # Providers resource class for GET /providers endpoint class Providers(Resource): def get(self): # Get the query parameters from the request and lowercase them active = request.args.get("active") if active is not None: active = active.lower() traits = request.args.get("traits") if traits is not None: traits = traits.lower() # Filter the providers by active if param given if active is not None: active = active == "true" providers = provider_collection.filter_by_active(active) else: providers = provider_collection.providers # Filter the providers by traits if given - example: trait1:value1|value2,trait2:value1|value2 if traits is not None: # Convert the traits param to a dictionary of lists and lowercase them traits_dict = {} for trait_list in traits.split(","): key, value_list = trait_list.split(":") traits_dict[key.lower()] = [value.lower() for value in value_list.split("|")] providers = provider_collection.filter_by_traits(traits_dict, providers) # Sort the providers by rating and frequency providers = provider_collection.sort_by_rating_and_popularity(providers) # Return the providers as a json response with their original values return {"providers": list(providers)} # Add the Providers resource to the api with the /providers endpoint api.add_resource(Providers, "/providers")

> Not technically what I was asking for but it did give me IncompleteTodos(Resource) so I can use this and refactor later. After a few modifications, the endpoint was up and running and I was off to debugging my code.

## Debugging /incomplete_todos

I have this: journal = Journal() @app.before_first_request def load_journal(): # Load the journal journal = journal.from_directory("/Users/elijahfry/code/notes/journal") But it gives me this error: File "/Users/elijahfry/code/providers-api-demo/index.py", line 19, in load_journal journal = journal.from_directory("/Users/elijahfry/code/notes/journal") UnboundLocalError: local variable 'journal' referenced before assignment

> having issues loading in files, they aren't even getting to the load step so its a problem with the walk and folder paths

## Fixing folder paths

> Eventually I got bing to generate this regex to use while working with the folder paths. 

r'([1-2][0-9]{3})/(0[1-9]|1[0-2])-(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)/([0-2][0-9]|3[0-1])_(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\.md'

Python - use this regex to find all markdown files that match the pattern in this path /Users/elijahfry/code/notes/journal "r'([1-2][0-9]{3})/(0[1-9]|1[0-2])-(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)/([0-2][0-9]|3[0-1])_(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\.md'"

> I finally fixed it with this:

```
match = re.match (r"^\s*-\s*(?:\[([x ])\]\s*)?(?:(?:<mark[^>]*>)?([\u263a-\U0001f645]+)(?:<\/mark>)?|(\d{1,2}:\d{2}))?(?:\s*(?:<mark[^>]*>)?([\u263a-\U0001f645]+)(?:<\/mark>)?|(\d{1,2}:\d{2}))?\s*(.+)$", line)
```

> And after dealing with that and modifying the match useage and todo returning a bit, it works! I have all 781 todos from my entire journal, plus all my journals loaded as data and I can work from here to add any functionality I would ever need.