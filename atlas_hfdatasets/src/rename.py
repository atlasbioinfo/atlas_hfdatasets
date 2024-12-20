import logging
from huggingface_hub import HfApi

def rename_dataset(repo_name, new_repo_name):
    """
    Rename a dataset repository on Hugging Face Hub
    
    Args:
        repo_name (str): Current repository name (format: username/repo_name)
        new_repo_name (str): New repository name (format: username/new_repo_name)
    """
    logging.info(f"Renaming dataset from {repo_name} to {new_repo_name}")
    
    try:
        api = HfApi()
        # Check if source repo exists
        try:
            api.dataset_info(repo_name)
        except Exception:
            logging.error(f"Source repository {repo_name} does not exist")
            return
            
        # Check if target repo already exists
        try:
            api.dataset_info(new_repo_name)
            logging.error(f"Target repository {new_repo_name} already exists")
            return
        except Exception:
            pass  # This is expected - target shouldn't exist
            
        # Confirm with user
        confirm = input(f"\nAre you sure you want to rename {repo_name} to {new_repo_name}? (y/N): ").lower()
        if confirm != 'y':
            logging.info("Rename operation cancelled by user")
            return
            
        # Perform the rename operation
        api.move_repo(
            from_id=repo_name,
            to_id=new_repo_name,
            repo_type="dataset"
        )
        
        logging.info(f"Successfully renamed dataset from {repo_name} to {new_repo_name}")
        
    except Exception as e:
        logging.error(f"Failed to rename dataset: {str(e)}")
