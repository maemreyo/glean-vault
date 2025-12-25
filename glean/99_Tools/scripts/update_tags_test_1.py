#!/usr/bin/env python3
import os
import re

FILES_TO_PROCESS = [
    "glean/40_Situation/It will be easy to find facts about this human geography aspect.md",
    "glean/40_Situation/New volunteers will start working in the week beginning? 2 Sep, 9 Sep, or 23 Sep.md",
    "glean/40_Situation/No useful research has been done on this human geography aspect.md",
    "glean/40_Situation/Rosie says that in her own city the main problem is? crime, housing or unemployment.md",
    "glean/40_Situation/The facts about this human geography aspect may not be reliable.md",
    "glean/40_Situation/The information given about aspects of human geography was too vague.md",
    "glean/40_Situation/The information given about this human geography aspect was too vague.md",
    "glean/40_Situation/The information provided about this human geography aspect was interesting.md",
    "glean/40_Situation/the role of the volunteers is collecting feedback on events.md",
    "glean/40_Situation/the role of the volunteers is contacting local businesses.md",
    "glean/40_Situation/the role of the volunteers is encouraging cooperation between local organisations.md",
    "glean/40_Situation/the role of the volunteers is giving advice to visitors.md",
    "glean/40_Situation/the role of the volunteers is helping people find their seats.md",
    "glean/40_Situation/the role of the volunteers is introducing guest speakers at an event.md",
    "glean/40_Situation/the role of the volunteers is providing entertainment.md",
    "glean/40_Situation/the role of the volunteers is providing publicity about a council service.md",
    "glean/40_Situation/the role of the volunteers is selling tickets.md",
    "glean/40_Situation/The students agree that developing disused industrial sites may? have unexpected costs, damage the urban environment or destroy valuable historical buildings.md",
    "glean/40_Situation/The students will mention Masdar City as an example of an attemp to achieve? daily collections for waste recycling, sustainable energy use or free transport for everyone.md",
    "glean/40_Situation/This human geography aspect may not be relevant to their course.md",
    "glean/40_Situation/This human geography aspect will involve only a small number of statistics.md",
    "glean/40_Situation/What is the most important requirement for volunteers at the festivals? interpersonal skills, personal interest in the event or flexibility.md",
    "glean/40_Situation/What is the next annual event for volunteers? A boat trip, a barbecue or a party.md",
    "glean/40_Situation/What recent additions to the outskirts of their cities are both students happy about? conference centres, sport centres or retail centres.md",
    "glean/40_Situation/When discussing the ecotown of Greenhill Abbots, Colin is uncertain about? what its objectives were, why there was opposition to it or how much of it has actually been built.md",
    "glean/40_Situation/Which event requires the largest number of volunteers? The music festival, the science festival, the book festival.md"
]

VAULT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
SLUG = "cam-20-test-1"
OLD_PREFIX = "#flashcards/ielts-listening/"
NEW_PREFIX = f"#flashcards/ielts-listening/{SLUG}/"

def process_file(rel_path):
    filepath = os.path.join(VAULT_ROOT, rel_path)
    if not os.path.exists(filepath):
        print(f"Skipping {rel_path}: File does not exist")
        return False
        
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    modified = False
    new_lines = []
    
    for line in lines:
        if line.strip().startswith(OLD_PREFIX) and NEW_PREFIX not in line:
            # Replace the old prefix with the new one containing the slug
            new_line = line.replace(OLD_PREFIX, NEW_PREFIX)
            new_lines.append(new_line)
            modified = True
        else:
            new_lines.append(line)
            
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"Updated {os.path.basename(rel_path)}")
        return True
    else:
        print(f"No changes needed for {os.path.basename(rel_path)}")
        return False

if __name__ == "__main__":
    print(f"Processing {len(FILES_TO_PROCESS)} files with slug {SLUG}...")
    updated_count = 0
    for f in FILES_TO_PROCESS:
        if process_file(f):
            updated_count += 1
    print(f"Finished. Updated {updated_count} files.")
