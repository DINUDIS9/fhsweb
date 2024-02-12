from flask import Flask, render_template, request
from fix_host_save import sav_to_json
import json
import os
import shutil
from flask_cors import CORS

uploads_folder = 'uploads'

# Check if the uploads folder exists, if not, create it
if not os.path.exists(uploads_folder):
    os.makedirs(uploads_folder)
    print("Uploads folder created successfully.")
else:
    print("Uploads folder already exists.")

# Automate the file overwrite by copying the new file over the existing one
level_json_path = os.path.join(uploads_folder, 'Level.json')
if os.path.exists(level_json_path):
    print("uploads/Level.json already exists, this will overwrite the file")
    # Ensure that Level.json is writable
    os.chmod(level_json_path, 0o777)
    print("Automatically proceeding with file overwrite")
    # Remove the existing Level.json
    os.remove(level_json_path)

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'folder_path' in request.files:
            level_sav_file = request.files['folder_path']
            if level_sav_file.filename == '':
                return "No file selected"
            if level_sav_file and level_sav_file.filename.endswith('.sav'):
                level_sav_file.save(os.path.join(uploads_folder, 'Level.sav'))
                sav_to_json(os.path.join(uploads_folder, 'Level.sav'), level_json_path)
                with open(level_json_path) as f:
                    level_json = json.load(f)
                players_json = [v['value']['RawData']['value']['object']['SaveParameter']['value'] for v in level_json['properties']['worldSaveData']['value']['CharacterSaveParameterMap']['value'] if 'IsPlayer' in v['value']['RawData']['value']['object']['SaveParameter']['value'] and v['value']['RawData']['value']['object']['SaveParameter']['value']['IsPlayer']['value']]
                players = [f'{v["NickName"]["value"]} (Lvl.{ v["Level"]["value"] if "Level" in v else "0"})' for v in players_json]
                return render_template('select_players.html', players=players)
            else:
                return "Invalid file format. Please select a .sav file."
    return render_template('index.html')

@app.route('/migrate', methods=['POST'])
def migrate():
    old_player_index = int(request.form['old_player'])
    new_player_index = int(request.form['new_player'])
    if old_player_index == new_player_index:
        return "You need to select different players for old and new accounts."
    else:
        return f"Migrating {request.form['old_player']} to {request.form['new_player']}"

if __name__ == '__main__':
    app.run(debug=True)
