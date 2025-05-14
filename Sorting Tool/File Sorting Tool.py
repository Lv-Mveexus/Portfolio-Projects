import os, shutil, json, logging

API_KEY = os.getenv("API_KEY")

# Set up logging configuration
logging.basicConfig(
    filename='file_sorting_tool.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load app information and credentials from config.json
app_config_path = r"C:\Users\Vuyisa M\Documents\Lv_Mveexus\Projects\Sorting Tool\app_config.json"
try:
    with open(app_config_path, 'r') as app_config_file:
        app_config = json.load(app_config_file)
        print(f"App Name: {app_config['app_name']}")
        logging.info("App Name: %s", app_config['app_name'])
        print(f"{app_config['app_name']} v{app_config['version']} by {app_config['author']}")
        logging.info("%s v%s by %s", app_config['app_name'], app_config['version'], app_config['author'])
except Exception as e:
    print(f"Error loading app configuration: {e}")
    logging.error("Error loading app configuration: %s", e)

#load configuration file
config_path = r"C:\Users\Vuyisa M\Documents\Lv_Mveexus\Projects\Sorting Tool\config.json"
try:
    with open(config_path, 'r') as config_file:
        folder_names = json.load(config_file)
        print("Loaded folder names:", folder_names)
        logging.info('Loaded folder names: %s', folder_names)
except Exception as e:
    print(f"Error loading configuration file: {e}")
    logging.error('Error loading configuration file: %s', e)
    folder_names = {}

if not all(isinstance(value, str) for value in folder_names.values()):
    raise ValueError("All values in folder_names must be strings.")

path = r"C:\Users\Vuyisa M\Downloads\\"
file_names = os.listdir(path)

# Create folders dynamically based on configuration
for folder in set(folder_names.values()):  
    folder_path = os.path.join(path, folder)
    if not os.path.exists(folder_path):
        print(f'Creating folder: {folder}')
        logging.info('Creating folder: %s', folder)
        os.makedirs(folder_path)
        
# Create "unknown" folder for unmapped files
unknown_folder = os.path.join(path, "unknown")
if not os.path.exists(unknown_folder):
    print('Creating folder: unknown')
    logging.info('Creating folder: unknown')
    os.makedirs(unknown_folder)
        
# Sort files into folders
for file in file_names:
    file_path = os.path.join(path, file)
    if os.path.isfile(file_path):  # Ensure the item is a file
        file_extension = file.split('.')[-1].lower()
        if file_extension in folder_names:  # Check if the file extension is in the folder_names mapping
            destination_folder = folder_names[file_extension]  # Get the corresponding folder name
            destination_path = os.path.join(path, destination_folder, file)  # Create the full destination path
            try:
                shutil.move(file_path, destination_path)  # Move the file to the destination folder
                print(f'Moved file: {file} to {destination_folder}')
                logging.info('Moved file: %s to %s', file, destination_folder)
            except Exception as e:
                print(f'Error moving file {file}: {e}')  # Handle any errors that occur during the move operation
                logging.error('Error moving file %s: %s', file, e)
        else:
            # Move file to "unknown" folder
            destination_path = os.path.join(unknown_folder, file)
            try:
                shutil.move(file_path, destination_path)
                print(f'Moved file: {file} to unknown folder')
                logging.info('Moved file: %s to unknown folder', file)
            except Exception as e:
                print(f'Error moving file {file} to unknown folder: {e}')
                logging.error('Error moving file %s to unknown folder: %s', file, e)
    else:
        print(f'Skipping folder: {file}')
        logging.info('Skipping folder: %s', file)
