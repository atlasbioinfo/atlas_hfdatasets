import logging,os,json
from src.core_functions import get_username
from huggingface_hub import DatasetInfo


def find_matching_datasets(dataset_pattern):
    """
    Find and display datasets matching the given pattern
    
    Args:
        dataset_pattern (str): Dataset pattern to match datasets
        
    Returns:
        list: List of matching dataset paths
    """
    import os
    import glob
    
    search_pattern = f"*{dataset_pattern}*"
    matching_datasets = [d for d in glob.glob(search_pattern) if os.path.isdir(d)]
    
    if not matching_datasets:
        logging.error(f"No dataset folders found matching pattern: {dataset_pattern}")
        logging.info("Current working directory: " + os.getcwd())
        logging.info("Available folders: " + str([d for d in os.listdir('.') if os.path.isdir(d)]))
        return None
    
    print("\nFound matching dataset folders:")
    print("-" * 60)
    for dataset_path in matching_datasets:
        dataset_name = os.path.basename(os.path.normpath(dataset_path))
        print(f"📁 {dataset_name}")
    print("-" * 60)
    print(f"\nTotal dataset folders found: {len(matching_datasets)}")
    
    return matching_datasets

def upload_dataset(dataset_pattern, repo_name=None, public=False):
    """
    Upload a local dataset to Hugging Face Dataset Hub
    
    Args:
        dataset_pattern (str): Dataset pattern to match datasets
        repo_name (str): Repository name for upload (format: username/repo_name). Default is the dataset folder name
        public (bool): Whether to make the dataset public (default: False)
    """
    logging.info("Uploading datasets to Hugging Face Dataset Hub")
    logging.info(f"Loading dataset from {dataset_pattern}")
    logging.info(f"Uploading to repository {repo_name}")

    try:
        from huggingface_hub import HfApi
        api = HfApi()
        api.dataset_info(repo_name)
        logging.info(f"Checked, repository {repo_name} exists")
    except Exception:
        logging.error(
            f"Repository {repo_name} does not exist, "
            f"please use \"atlas_hfdatasets create {repo_name}\" to create it first..."
        )
        return
        
    matching_datasets = find_matching_datasets(dataset_pattern)
    if not matching_datasets:
        return
    
    confirm = input("\nDo you want to upload these datasets? (y/N): ").lower()
    if confirm != 'y':
        logging.info("Upload cancelled by user")
        return
    from datasets import load_from_disk
    from huggingface_hub import create_repo

    for dataset_path in matching_datasets:
        try:
            dataset = load_from_disk(dataset_path)
            config_name = os.path.basename(os.path.normpath(dataset_path))
            
            # 上传数据集
            dataset.push_to_hub(
                repo_id=repo_name,
                private=not public,
                config_name=config_name
            )
            
            logging.info(f"Successfully uploaded dataset to {repo_name} with config {config_name}")
            
        except Exception as e:
            logging.error(f"Failed to upload dataset {dataset_path}: {str(e)}")
            continue
    
    logging.info("Dataset upload process completed")
