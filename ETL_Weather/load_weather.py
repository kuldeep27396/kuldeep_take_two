import pandas as pd

def load_to_csv(input_path, output_path):
    try:
        df = pd.read_csv(input_path)

        df.to_csv(output_path, index=False)

        print(f"Successfully loaded data from {input_path} to {output_path}")
    except Exception as e:
        print(f"Error loading data from {input_path} to {output_path}: {e}")

def main():
    load_to_csv("transformed_weather_data.csv", "loaded_transformed_weather_data.csv")
    load_to_csv("daily_weather_summary.csv", "loaded_daily_weather_summary.csv")

if __name__ == "__main__":
    main()
