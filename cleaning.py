import pandas as pd
import re
from urllib.parse import urlparse, urlunparse
from typing import Optional, List

# --- 1. ZIP Code Extraction Function ---

def extract_zip_code(address: str) -> Optional[str]:
    """
    Extracts a 5-digit or 5+4-digit ZIP code from a string using regex.

    Args:
        address (str): The full address string.

    Returns:
        Optional[str]: The extracted ZIP code (e.g., '10036' or '90210-1234'), 
                       or None if not found or input is NaN.
    """
    if pd.isna(address):
        return None
    
    # Regex pattern to find 5 digits, optionally followed by a hyphen and 4 more digits.
    # It looks for patterns common in US addresses, often preceded by a space and a state abbreviation.
    match = re.search(r'(\d{5}(?:-\d{4})?)(?:\D|$)', str(address))
    
    if match:
        return match.group(1)
    return None


# --- 2. Link Shortening/Cleaning Function ---

def clean_and_normalize_url(url: str) -> str:
    """
    Cleans and normalizes a URL by stripping tracking parameters (query and fragment).
    
    Args:
        url (str): The original URL string.

    Returns:
        str: The cleaned URL (scheme, netloc, and path only), or the original 
             value if not a valid URL format.
    """
    if pd.isna(url) or not isinstance(url, str) or not url.strip().startswith(('http', 'www')):
        return url

    try:
        # Parse the URL into its components
        parsed = urlparse(url)
        
        # Rebuild the URL using only the scheme, netloc (domain), and path.
        # This removes tracking query parameters and fragments.
        cleaned_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, 
                                  '', # params
                                  '', # query
                                  '')) # fragment
        
        # Ensure 'http://' or 'https://' is present for a valid link structure
        if not cleaned_url.startswith('http'):
            # Use 'https' as the default scheme if none was specified
            cleaned_url = 'https://' + cleaned_url.lstrip('/')
            
        return cleaned_url

    except Exception as e:
        print(f"Error cleaning URL {url}: {e}")
        return url


# --- 3. Main Processing Logic ---

def process_data(file_path: str, name_col: str, address_col: str, website_col: str):
    """
    Reads the data, applies the cleaning functions using specified column names, 
    and prints the result, and saves the cleaned data to a new CSV file.
    """
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path)
        print(f"--- Successfully loaded {len(df)} records from {file_path} ---")
        
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}. Please check the file path.")
        return
    except Exception as e:
        print(f"An error occurred during file loading: {e}")
        return

    # Check for required columns
    required_cols = [name_col, address_col, website_col]
    missing_cols = [col for col in required_cols if col not in df.columns]

    print(f"DataFrame columns loaded: {df.columns.tolist()}")

    if missing_cols:
        print(f"\nFATAL ERROR: The following required columns are missing from the CSV: {missing_cols}")
        print("Please update the column names in the CONFIGURATION section below to match your CSV file.")
        return

    # 1. Apply Zip Code Extraction
    print("\n--- Extracting Zip Codes ---")
    # This creates the new column, usually appended to the end of the DataFrame.
    df['Zip Code'] = df[address_col].apply(extract_zip_code)

    # 2. Apply URL Cleaning
    print("--- Cleaning and Normalizing URLs (Overwriting original column) ---")
    # Overwrite the original Website column with the cleaned URLs
    df[website_col] = df[website_col].apply(clean_and_normalize_url)
    
    # --- NEW LOGIC: Reorder Columns for Display and Save ---
    
    # Get the current column list
    current_cols = df.columns.tolist()
    zip_col_name = 'Zip Code'
    
    # 1. Remove the new Zip Code column from its default appended position
    if zip_col_name in current_cols:
        current_cols.remove(zip_col_name)
    
    # 2. Find the index of the address column
    try:
        address_index = current_cols.index(address_col)
    except ValueError:
        print(f"Error: Address column '{address_col}' not found for reordering.")
        return
        
    # 3. Insert the Zip Code column immediately after the address column
    current_cols.insert(address_index + 1, zip_col_name)
    
    # 4. Reindex the DataFrame to apply the new, desired column order
    df = df.reindex(columns=current_cols)
    
    # --- END NEW LOGIC ---

    # Display the new DataFrame with the extracted and cleaned columns
    print("\n--- Final Cleaned DataFrame (showing relevant columns) ---")
    
    # Dynamically select and display the columns (order is now correct)
    display_cols: List[str] = [name_col, address_col, 'Zip Code', website_col]
    print(df[display_cols])

    # To save the results to a new CSV file:
    output_file_name = 'cleaned_restaurants_output.csv'
    # The saved file will now have 'Zip Code' right after 'Address'
    df.to_csv(output_file_name, index=False)
    print(f"\nResults successfully saved to '{output_file_name}'")


if __name__ == "__main__":
    # --- CONFIGURATION (UPDATE THESE VALUES TO MATCH YOUR FILE) ---
    # Based on your previous run, this is the expected file name:
    data_file = 'restaurants_New_York_city_Yonkers_buffalo_leads.csv' 
    
    # NOTE: Set the exact column headers from your CSV file here.
    COL_NAME = 'Place' # <-- This is the current working value, or adjust if needed.
    COL_ADDRESS = 'Address'
    COL_WEBSITE = 'Website'
    # ----------------------------------------------------------------

    # Use the function with the configured columns
    process_data(data_file, COL_NAME, COL_ADDRESS, COL_WEBSITE)
