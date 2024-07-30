import pandas as pd
import json

# Specify the path to the CSV file / CVS dosyasının yolu
csv_file_path = "mnt\data\EsAnlamlilar.csv"

# Read the CVS file / CVS dosyasını oku
df = pd.read_csv(csv_file_path)

# Let's display the first few rows of the CVS file / CVS dosyasının birkaç satırını görüntüleme
print(df.head())

# Create a dictionary to convert synonyms to json format /eş anlamlıları json formatına dönüştürmek için bir sözlük oluşturma
synonyms_dict = {}
for index, row in df.iterrows():
    key = row[0]
    values = row[1].split(',')  # Convert synonyms into a list by splitting them with a comma / eş anlamlıları virgülle ayırarak bir listeye dönüştürme
    synonyms_dict[key] = values

# convert to json format / JSON formatına dönüştür
json_output = json.dumps(synonyms_dict, ensure_ascii=False, indent=4)

# save the json output to a file / JSON çıktısını bir dosyaya kaydet
json_file_path = "mnt/data/synonyms.json"
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json_file.write(json_output)

print("JSON formatına dönüştürüldü ve kaydedildi:", json_file_path)
