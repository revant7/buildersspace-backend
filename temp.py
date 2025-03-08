import chardet

with open("sample_data.csv", "rb") as f:
    raw_data = f.read()

encoding = chardet.detect(raw_data)["encoding"]
print(f"Detected Encoding: {encoding}")

with open("sample_data.csv", "r", encoding=encoding) as f:
    data = f.read()
