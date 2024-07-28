import pandas as pd
import json

# CSV dosyasının yolunu belirtin
csv_file_path = "mnt\data\EsAnlamlilar.csv"

# CSV dosyasını oku
df = pd.read_csv(csv_file_path)

# CSV dosyasının ilk birkaç satırını görüntüleyelim
print(df.head())

# Eş anlamlıları JSON formatına dönüştürmek için bir sözlük oluştur
synonyms_dict = {}
for index, row in df.iterrows():
    key = row[0]
    values = row[1].split(',')  # Eş anlamlıları virgülle ayırarak bir listeye dönüştür
    synonyms_dict[key] = values

# JSON formatına dönüştür
json_output = json.dumps(synonyms_dict, ensure_ascii=False, indent=4)

# JSON çıktısını bir dosyaya kaydet
json_file_path = "mnt/data/synonyms.json"
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json_file.write(json_output)

print("JSON formatına dönüştürüldü ve kaydedildi:", json_file_path)
