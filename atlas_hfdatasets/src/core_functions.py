import logging, argparse,os,sys


def login_to_hub():
    try:
        from huggingface_hub import HfApi
        api = HfApi()
        user_info = api.whoami()
        print("\nSuccessfully logged in to Hugging Face Hub!")
        print(f"Welcome ({user_info['name']})")

        print("\n=== User Information ===")
        print(f"Username: {user_info['name']}")
        print(f"Full Name: {user_info['fullname']}")
        print(f"==========================")
        print("\n")
    except Exception:
        # Not logged in, prompt for login
        print("Please login to Hugging Face Hub first.")
        print("You can get your access token from https://huggingface.co/settings/tokens")
        token = input("Enter your Hugging Face access token: ").strip()
        
        # Login with provided token
        from huggingface_hub import login
        try:
            login(token=token)
            print("Successfully logged in to Hugging Face Hub!")
            from huggingface_hub import HfApi
            api = HfApi()
            user_info = api.whoami()
        except Exception as e:
            print(f"Login failed: {str(e)}")
            sys.exit(1)
    
    atlas_path = os.path.expanduser("~/.atlas")
    if not os.path.exists(atlas_path):
        os.makedirs(atlas_path)

    username_file = os.path.join(atlas_path, "hf_username.info")
    
    with open(username_file, "w") as f:
        f.write(user_info['name'])
    

def get_username():
    """
    Get the Hugging Face username from the stored info file
    
    Returns:
        str: The username stored in ~/.atlas/hf_username.info
    """
    atlas_path = os.path.expanduser("~/.atlas")
    username_file = os.path.join(atlas_path, "hf_username.info")
    
    if not os.path.exists(username_file):
        logging.error("Username info not found. Please login first.")
        sys.exit(1)
        
    with open(username_file, "r") as f:
        username = f.read().strip()
        
    return username


def remove_dataset(repo_name, force=False):
    """
    Remove a dataset from the Hugging Face Hub.
    
    Args:
        repo_name (str): Name of the repository to remove (format: username/repo_name)
        force (bool): Whether to force deletion without confirmation
    """
    
    logging.info(f"Removing dataset {repo_name} from Hugging Face Dataset Hub")
    
    if not force:
        confirm = input(f"Are you sure you want to delete dataset {repo_name}? This cannot be undone. [y/N]: ")
        if confirm.lower() != 'y':
            logging.info("Deletion cancelled")
            return
            
    from huggingface_hub import delete_repo
    delete_repo(repo_name, repo_type="dataset")
    logging.info(f"Dataset {repo_name} successfully removed")

def list_datasets(keyword=None, username=None):
    """
    List datasets available on Hugging Face Hub for a given user
    
    Args:
        keyword (str): Filter datasets by keyword (case-insensitive)
        username (str): Your Hugging Face username
    """
    if username is None:
        try:
            username = get_username()
        except Exception as e:
            logging.error(f"Error getting username: {str(e)}")
            logging.error(".")
            sys.exit(1)
        
    from huggingface_hub import HfApi
    import re
    api = HfApi()
    try:
        logging.info("Retrieving dataset list from Hugging Face Hub...")
        datasets = api.list_datasets(author=username)
        if datasets:
            # Filter datasets by keyword if provided
            if keyword:
                pattern = re.compile(keyword, re.IGNORECASE)
                datasets = [d for d in datasets if pattern.search(d.id)]
            
            if datasets:
                print("\nFound following datasets on Hugging Face Hub:")
                print("\n{:<40} {:<25} {:<10} {:<30}".format(
                    "Dataset ID", "Last Modified", "Downloads", "Tags"))
                print("-" * 105)
                
                for dataset in datasets:
                    tags = ', '.join(dataset.tags) if dataset.tags else ''
                    print("{:<40} {:<25} {:<10} {:<30}".format(
                        dataset.id,
                        dataset.lastModified,
                        str(dataset.downloads),
                        tags[:30] + ('...' if len(tags) > 30 else '')
                    ))
            else:
                print(f"\nNo matching datasets found for keyword '{keyword}'")
        else:
            print(f"\nNo datasets found for user {username} on Hugging Face Hub")
    except Exception as e:
        logging.error(f"Error retrieving datasets: {str(e)}")

def upload_dataset(dataset_path, repo_name=None, public=False):
    """
    Upload a local dataset to Hugging Face Dataset Hub
    
    Args:
        dataset_path (str): Path to the local dataset
    """
    logging.basicConfig(level=logging.INFO)
    logging.info("Uploading datasets to Hugging Face Dataset Hub")
    logging.info(f"Loading dataset from {dataset_path}")
    
    from datasets import load_from_disk
    import os
    dataset = load_from_disk(dataset_path)
    
    if repo_name is None:
        # Use the dataset folder name as repo name
        repo_name = os.path.basename(os.path.normpath(dataset_path))
    
    dataset.push_to_hub(repo_name, private=not public)
    logging.info(f"Dataset successfully uploaded to {repo_name} as {'public' if public else 'private'}")

def download_dataset(repo_name, output_dir):
    """
    Download a dataset from Hugging Face Hub
    
    Args:
        repo_name (str): Repository name in format username/repo_name
        output_dir (str): Local directory to save the dataset
    """
    logging.info(f"Downloading dataset from {repo_name}")
    try:
        from datasets import load_dataset
        dataset = load_dataset(repo_name)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Save dataset to disk
        output_path = os.path.join(output_dir, repo_name.split('/')[-1])
        dataset.save_to_disk(output_path)
        logging.info(f"Dataset successfully downloaded to {output_path}")
        
    except Exception as e:
        logging.error(f"Failed to download dataset: {str(e)}")
        raise

def check_dataset(repo_name):
    """
    Check dataset statistics from Hugging Face Hub
    """
    from huggingface_hub import HfApi
    api = HfApi()
    dataset_info = api.dataset_info(repo_name)
    print("\n=== Dataset Information ===")
    print(f"ID: {dataset_info.id}")
    print(f"Author: {dataset_info.author}")
    print(f"Created: {dataset_info.created_at}")
    print(f"Last Modified: {dataset_info.last_modified}")
    print(f"Private: {dataset_info.private}")
    print(f"Downloads: {dataset_info.downloads}")
    print(f"Likes: {dataset_info.likes}")
    print(f"Tags: {dataset_info.tags}")
    
    if dataset_info.card_data and dataset_info.card_data.get('dataset_info'):
        info = dataset_info.card_data['dataset_info']
        print("\n=== Dataset Statistics ===")
        print("Features:")
        for feature in info['features']:
            print(f"  - {feature['name']} ({feature['dtype']})")
        
        print("\nSplits:")
        for split in info['splits']:
            print(f"  - {split['name']}: {split['num_examples']} examples")
        
        print(f"\nDownload Size: {info['download_size']} bytes")
        print(f"Dataset Size: {info['dataset_size']} bytes")
    
    print("\n=== Files ===")
    for sibling in dataset_info.siblings:
        print(f"  - {sibling.rfilename}")
    print("=======================\n")
