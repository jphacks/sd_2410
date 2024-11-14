import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.my_socket import my_config, socket_com
import json
import pandas as pd

while 1:
    socket_get_data = socket_com.start_server_getString()
    data = json.loads(socket_get_data)
    speaker_id = data['speaker_id']
    speaker_name = data['speaker_name']
    speaker_mate = data['speaker_mate']

    csv_dic = {
        "speaker_id" : [speaker_id],
        "speaker_name": [speaker_name],
        "spealer_mate": [speaker_mate]
    }
    csv_df = pd.DataFrame(csv_dic)
    csv_df.to_csv("speaker.csv", index=False)