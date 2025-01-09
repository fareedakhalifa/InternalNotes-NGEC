# Notes To Self for Using NGEC

> When using the geoparser, ensure that an elastic search is run using `sudo docker run -d -p 127.0.0.1:9200:9200 -e "discovery.type=single-node" -v ./geonames_index/:/usr/share/elasticsearch/data elasticsearch:7.17.9`

Next, follow David's steps and edit the `NGEC/examples/demo_mordecai.py` file

The full code for the file should look like this - it includes parts to decrease the output size:
```
import importlib.resources
from mordecai3 import Geoparser
from pprint import pprint

# Suppress warnings
import warnings
warnings.filterwarnings("ignore")

# Silence noisy logging from specific libraries
import logging
logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger("elasticsearch").setLevel(logging.CRITICAL)
logging.getLogger("transformers").setLevel(logging.CRITICAL)

geo = Geoparser(importlib.resources.files("mordecai3") / "assets/mordecai_2024-06-04.pt")

output = geo.geoparse_doc("The Mexican government sent 300 National Guard troopers to bolster the southern state of Guerrero on Tuesday, where a local police chief and 12 officers were shot dead in a brutal ambush the day before.")

pprint(output)
```

❖ In this case, the output is as follows:
```
/opt/anaconda3/envs/ngec_trial2/lib/python3.10/site-packages/transformers/utils/generic.py:441: FutureWarning: `torch.utils._pytree._register_pytree_node` is deprecated. Please use `torch.utils._pytree.register_pytree_node` instead.
  _torch_pytree._register_pytree_node(
/opt/anaconda3/envs/ngec_trial2/lib/python3.10/site-packages/transformers/utils/generic.py:309: FutureWarning: `torch.utils._pytree._register_pytree_node` is deprecated. Please use `torch.utils._pytree.register_pytree_node` instead.
  _torch_pytree._register_pytree_node(
2025-01-09 12:23:57,604 root         DEBUG    **Place name**: Guerrero
2025-01-09 12:23:57,605 root         DEBUG    Picking top predicted result
{'doc_text': 'The Mexican government sent 300 National Guard troopers to '
             'bolster the southern state of Guerrero on Tuesday, where a local '
             'police chief and 12 officers were shot dead in a brutal ambush '
             'the day before.',
 'event_location_raw': '',
 'geolocated_ents': [{'admin1_code': '06',
                      'admin1_name': 'Chihuahua',
                      'admin2_code': '031',
                      'admin2_name': 'Guerrero',
                      'city_id': '4013716',
                      'city_name': 'Guerrero',
                      'country_code3': 'MEX',
                      'end_char': 97,
                      'feature_class': 'P',
                      'feature_code': 'PPLA2',
                      'geonameid': '4013716',
                      'lat': 28.54875,
                      'lon': -107.48377,
                      'name': 'Guerrero',
                      'score': 0.40141481161117554,
                      'search_name': 'Guerrero',
                      'start_char': 89}]}
```

❖ I have also added a new option to save the output into a csv file - if it is fed manually, if we feed it through an existing CSV, please check the other code (`demo_mordecai_FK3`)
```
import csv

# Define the CSV headers
csv_file = "output.csv"
headers = [
    'doc_text', 'name', 'lat', 'lon', 'country_code3', 'admin1_name',
    'admin2_name', 'feature_code', 'start_char', 'end_char'
]

# Initialize the CSV file with headers if it doesn't already exist
try:
    with open(csv_file, mode='x', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
except FileExistsError:
    # If the file exists, skip writing the header
    pass

# Function to add new rows for each processed doc_text
def save_to_csv(output):
    geolocated_ents = output.get('geolocated_ents', [])
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        for ent in geolocated_ents:
            writer.writerow({
                'doc_text': output['doc_text'],
                'name': ent.get('name', ''),
                'lat': ent.get('lat', ''),
                'lon': ent.get('lon', ''),
                'country_code3': ent.get('country_code3', ''),
                'admin1_name': ent.get('admin1_name', ''),
                'admin2_name': ent.get('admin2_name', ''),
                'feature_code': ent.get('feature_code', ''),
                'start_char': ent.get('start_char', ''),
                'end_char': ent.get('end_char', ''),
            })
    print(f"Added to {csv_file}")
```
