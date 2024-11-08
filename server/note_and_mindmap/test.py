from model import *


generator = MindmapNoteGenerator(input_path="text.txt", output_note_path="output/notes.json", output_mindmap_path="output/mindmap.json")

# Read content from the input file
generator.read_file()

# Generate notes and mindmap
generator.generate_note()
generator.generate_mindmap()