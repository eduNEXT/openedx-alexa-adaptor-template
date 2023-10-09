"""
Script to load the permissions in the skill.json
from the sample-skill into the new skill
"""
import json
import sys

NEW_SKILL_FOLDER = sys.argv[1]

SAMPLE_SKILL_PATH = "sample-skill/skill-package/skill.json"
with open(SAMPLE_SKILL_PATH, "r", encoding="utf-8") as original_manifest:
    permissions = json.load(original_manifest)["manifest"]["permissions"]

NEW_SKILL_PATH = f"skills/{NEW_SKILL_FOLDER}/skill-package/skill.json"
with open(NEW_SKILL_PATH, "r+", encoding="utf-8") as new_manifest:
    updated_manifest = json.load(new_manifest)
    updated_manifest["manifest"]["permissions"] = permissions
    new_manifest.seek(0)
    json.dump(updated_manifest, new_manifest, indent=2)
    new_manifest.truncate()
