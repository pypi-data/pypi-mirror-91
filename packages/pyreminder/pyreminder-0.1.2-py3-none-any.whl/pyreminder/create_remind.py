from .constants import PROPERTY_TYPES
import os

NEW_REMINDER = '''
osascript -e \
'tell application "Reminders"
make new reminder with properties {%s}
end tell'
'''

def new_reminder(task):
    property_strings = []
    for key in task:
        if PROPERTY_TYPES[key] == "text":
            property_strings.append('%s:"%s"' % (key, task[key]))
        elif PROPERTY_TYPES[key] == "date":
            property_strings.append('%s:date "%s"' % (key, task[key]))
        else:
            property_strings.append('%s:%s' % (key, task[key]))
    new_reminder_cmd = NEW_REMINDER % ', '.join(property_strings)
    os.system(new_reminder_cmd)
