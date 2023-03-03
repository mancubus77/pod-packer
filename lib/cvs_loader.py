import csv


def csv_to_json(csv_path) -> list:
    """
    Map CSV to JSON
    :param csv_path: Path to CSV file
    :return: List of dicts
    """
    json_ds = []
    with open(csv_path) as csv_file:
        csv_r = csv.DictReader(csv_file)
        for row in csv_r:
            row["affinity"] = row["affinity"] if row["affinity"] != "" else "1"
            json_ds.append(row)
    return json_ds
