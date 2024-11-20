import logging, argparse,os,sys
from huggingface_hub import create_repo

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
    try:
        from huggingface_hub import HfApi
        api = HfApi()
        api.repo_info(repo_id=repo_name, repo_type="dataset")
        logging.info(f"Checked: Dataset repository {repo_name} exists")
    except Exception as e:
        logging.error(f"Dataset repository {repo_name} does not exist: {str(e)}")
        return
    if not force:
        confirm = input(f"Are you sure you want to delete dataset {repo_name}? This cannot be undone. [y/N]: ")
        if confirm.lower() != 'y':
            logging.info("Deletion cancelled")
            return
            
    from huggingface_hub import delete_repo
    delete_repo(repo_name, repo_type="dataset")
    logging.info(f"Dataset {repo_name} successfully removed")


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

def create_dataset(repo_name: str, public: bool = False) -> None:
    """
    Create a new empty dataset repository on Hugging Face Hub.
    
    Args:
        repo_name (str): Name of the repository to create (format: username/repo_name)
        public (bool): Whether to make the dataset public (default: False)
    """
    try:
        create_repo(
            repo_id=repo_name,
            repo_type="dataset",
            private=not public,
        )
        logging.info(f"Successfully created dataset repository: {repo_name}")
    except Exception as e:
        logging.error(f"Failed to create dataset repository: {str(e)}")
        sys.exit(1)