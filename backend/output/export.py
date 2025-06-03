import os


def export_tables(model_dict, output_dir="data"):
    """
    Export each DataFrame in the model dictionary to a CSV file.

    Parameters:
        model_dict (dict): Mapping of table name → pandas DataFrame
        output_dir (str): Directory where CSVs will be saved (will be created if not exists)
    """
    os.makedirs(output_dir, exist_ok=True)
    for name, df in model_dict.items():
        filename = f"{name}.csv"
        filepath = os.path.join(output_dir, filename)
        df.to_csv(filepath, index=False)
        print(f"✔️ Exported '{name}' ({len(df)} rows) to {filepath}")


if __name__ == '__main__':
    # Example usage
    from auth.spotify_auth import authenticate_user
    from transform.model import build_model

    sp = authenticate_user()
    model = build_model(sp, limit=20)
    export_tables(model)
