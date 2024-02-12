from flask import Flask, render_template, request
from fix_host_save import sav_to_json, apply_fix
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    print("Hello World")
    return "Hello World"

@app.route('/migrate', methods=['POST'])
def migrate():
    players_json = None
    selected_file = request.form['folder_path']
    old_player_index = int(request.form['old_player'])
    new_player_index = int(request.form['new_player'])

    # Perform migration logic
    # Adapt this part to use your existing migration logic
    player_folder_path = os.path.join(os.path.dirname(selected_file), "Players")
    new_player_guid = players_json[new_player_index]["key"]["PlayerUId"]["value"].replace("-", "").upper()
    old_player_guid = players_json[old_player_index]["key"]["PlayerUId"]["value"].replace("-", "").upper()
    apply_fix(
        os.path.join(player_folder_path, f"{new_player_guid}.sav"),
        os.path.join(player_folder_path, f"{old_player_guid}.sav")
    )

    return "Migration completed successfully"

if __name__ == '__main__':
    app.run(debug=True)
