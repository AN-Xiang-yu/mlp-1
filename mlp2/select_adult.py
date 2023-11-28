
import json
from pandas import json_normalize
from typing import Dict,Any


def check_adult_limit(json_data: str) -> str:
    """
    Converts a JSON string containing movie data into a DataFrame, filters specific columns,
    and returns the filtered data as a JSON string.

    Args:
        json_data (str): A JSON string representation of movie data.

    Returns:
        str: A JSON string containing filtered data with columns 'adult', 'original_title',
        and 'overview'.

    This function parses the input JSON string into a DataFrame, selects specific columns
    relevant to movie information, and then converts the filtered DataFrame back into
    a JSON string. It's particularly used for processing movie data to focus on adult
    classification, title, and overview.
    """
    # Parse the JSON string into a DataFrame
    df = json_normalize(json.loads(json_data))

    # Select the relevant columns
    df = df[['adult', 'original_title', 'overview']]

    # Convert the DataFrame to a JSON string and return
    return df.to_json(orient='records')