


def list_datasets(keyword=None, username=None):
    import logging
    import sys
    """
    List datasets available on Hugging Face Hub for a given user
    
    Args:
        keyword (str): Filter datasets by keyword (case-insensitive)
        username (str): Your Hugging Face username
    """
        
    from huggingface_hub import HfApi
    from datasets import get_dataset_config_names
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
                print("-" * 80)
                
                if keyword:
                    # 详细显示带关键词过滤的数据集信息
                    for dataset in datasets:
                        tags = ', '.join(dataset.tags) if dataset.tags else 'No tags'
                        separator = "=" * 80
                        
                        print(f"\nDataset: {dataset.id}")
                        print(f"Last Modified: {dataset.lastModified}")
                        print(f"Downloads: {dataset.downloads}")
                        print(f"Tags: {tags}")
                        
                        try:
                            configs = get_dataset_config_names(dataset.id)
                            print("Configs:")
                            if configs:
                                for config in configs:
                                    print(f"  - {config}")
                            else:
                                print("  - No configs available")
                        except Exception:
                            print("Configs: Error loading configs")
                        
                        print(separator)
                        print()
                else:
                    # 只显示数据集名称列表
                    for dataset in datasets:
                        print(f"- {dataset.id}")
                    print()
            else:
                print(f"\nNo matching datasets found for keyword '{keyword}'")
        else:
            print(f"\nNo datasets found for user {username} on Hugging Face Hub")
    except Exception as e:
        logging.error(f"Error retrieving datasets: {str(e)}")