# scripts/clean_coordinates.py
import pandas as pd

df = pd.read_csv('./raw/hospital_directory.csv', low_memory=False)

# Parse Location_Coordinates ("lat, long" format) into separate columns
df = df.dropna(subset=['Location_Coordinates'])
coords = df['Location_Coordinates'].str.split(',', expand=True)
df['latitude'] = pd.to_numeric(coords[0].str.strip(), errors='coerce')
df['longitude'] = pd.to_numeric(coords[1].str.strip(), errors='coerce')

# Remove rows with invalid coordinates
df = df.dropna(subset=['latitude', 'longitude'])
df = df[(df['latitude'].between(6, 38)) & (df['longitude'].between(68, 98))]  # India bounds

print(f"Total valid records: {len(df)}")
print(f"Sample coordinates:\n{df[['Hospital_Name', 'State', 'latitude', 'longitude']].head()}")

# Save cleaned data
df.to_csv('./processed/hospitals_clean.csv', index=False)