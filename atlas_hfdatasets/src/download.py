import logging, os

def download_dataset(repo_name, output_dir):
    """
    Download a dataset from Hugging Face Hub with all its configurations
    
    Args:
        repo_name (str): Repository name in format username/repo_name
        output_dir (str): Local directory to save the dataset
    """
    logging.info(f"Downloading dataset from {repo_name}")
    try:
        from datasets import load_dataset, get_dataset_config_names
        
        # Get all available configs
        configs = get_dataset_config_names(repo_name)
        logging.info(f"Found {len(configs)} configurations")
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Download each configuration
        for config in configs:
            logging.info(f"Downloading configuration: {config}")
            dataset = load_dataset(repo_name, config)
            
            # Save dataset to disk
            output_path = os.path.join(output_dir, repo_name.split('/')[-1], config)
            dataset.save_to_disk(output_path)
            logging.info(f"Configuration {config} downloaded to {output_path}")
            
    except Exception as e:
        logging.error(f"Failed to download dataset: {str(e)}")
        raise