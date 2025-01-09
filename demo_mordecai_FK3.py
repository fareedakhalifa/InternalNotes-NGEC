# Import required libraries
import importlib.resources
from mordecai3 import Geoparser
import warnings
import logging
import csv

# Suppress warnings and logging
warnings.filterwarnings("ignore")
logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger("elasticsearch").setLevel(logging.CRITICAL)
logging.getLogger("transformers").setLevel(logging.CRITICAL)

# Initialize the Geoparser
geo = Geoparser(importlib.resources.files("mordecai3") / "assets/mordecai_2024-06-04.pt")

# Define input and output file paths
input_csv = "./NGEC/Input/sentences.csv"  # Input file with sentences and IDs
output_csv = "./NGEC/Geoparser Output/output.csv"  # Output file path

# Define CSV headers for the output
headers = [
    'sentence_id', 'doc_text', 'name', 'lat', 'lon', 'country_code3', 
    'admin1_name', 'admin2_name', 'feature_code', 'start_char', 'end_char'
]

# Create the output CSV if it doesn't exist
try:
    with open(output_csv, mode='x', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
except FileExistsError:
    # If the file exists, skip writing the header
    pass

# Function to save geoparser output to CSV
def save_to_csv(sentence_id, output):
    geolocated_ents = output.get('geolocated_ents', [])
    with open(output_csv, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        for ent in geolocated_ents:
            writer.writerow({
                'sentence_id': sentence_id,  # Corrected to use the passed argument
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
    print(f"Processed sentence ID {sentence_id} and added to {output_csv}")

# Batch process sentences from the input CSV
with open(input_csv, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        sentence_id = row['sentence_id']  # Ensure this matches the input CSV's header
        doc_text = row['doc_text']  # Ensure this matches the input CSV's header
        try:
            # Process the sentence with the geoparser
            output = geo.geoparse_doc(doc_text)
            # Save the output to the CSV
            save_to_csv(sentence_id, output)
        except Exception as e:
            print(f"Error processing sentence ID {sentence_id}: {e}")
