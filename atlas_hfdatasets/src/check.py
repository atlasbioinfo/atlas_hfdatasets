def check_dataset(repo_name):
    """
    Check dataset statistics from Hugging Face Hub
    """

    from huggingface_hub import HfApi
    api = HfApi()

    dataset_info = api.dataset_info(repo_name)
    
    print("=======================\n")
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
        configs = info if isinstance(info, list) else [info]
        
        for dataset_config in configs:
            if config_name := dataset_config.get('config_name'):
                print(f"\nConfig: {config_name}")
            
            if description := dataset_config.get('description'):
                print(f"Description: {description}")
            
            if features := dataset_config.get('features'):
                print("\nFeatures:")
                for feature in features:
                    print(f"  - {feature['name']} ({feature['dtype']})")
            
            if splits := dataset_config.get('splits'):
                print("\nSplits:")
                for split in splits:
                    print(f"  - {split['name']}: {split['num_examples']} examples")
                    print(f"    Size: {split['num_bytes'] / (1024 * 1024):.2f} MB")
            
            if download_size := dataset_config.get('download_size'):
                print(f"\nDownload Size: {download_size / (1024 * 1024):.2f} MB")
            if dataset_size := dataset_config.get('dataset_size'):
                print(f"Dataset Size: {dataset_size / (1024 * 1024):.2f} MB")
    
    print("\n=== Files ===")
    for sibling in dataset_info.siblings:
        print(f"  - {sibling.rfilename}")
    

