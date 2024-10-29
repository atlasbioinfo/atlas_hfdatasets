import logging, argparse,os

def remove_dataset(repo_name, force=False):
    """
    Remove a dataset from the Hugging Face Hub.
    
    Args:
        repo_name (str): Name of the repository to remove (format: username/repo_name)
        force (bool): Whether to force deletion without confirmation
    """
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Removing dataset {repo_name} from Hugging Face Dataset Hub")
    
    if not force:
        confirm = input(f"Are you sure you want to delete dataset {repo_name}? This cannot be undone. [y/N]: ")
        if confirm.lower() != 'y':
            logging.info("Deletion cancelled")
            return
            
    from huggingface_hub import delete_repo
    delete_repo(repo_name, repo_type="dataset")
    logging.info(f"Dataset {repo_name} successfully removed")

def list_datasets(username, keyword=None):
    """
    List datasets available on Hugging Face Hub for a given user
    
    Args:
        username (str): Hugging Face username
        keyword (str): Filter datasets by keyword (case-insensitive)
    """
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


def main():
    logging.basicConfig(level=logging.INFO)
    
    logo=r'''
          _   _             ____  _       _        __
     /\  | | | |           |  _ \(_)     (_)      / _|
    /  \ | |_| | __ _ ___  | |_) |_  ___  _ _ __ | |_ ___
   / /\ \| __| |/ _` / __| |  _ <| |/ _ \| | '_ \|  _/ _ \
  / ____ \ |_| | (_| \__ \ | |_) | | (_) | | | | | || (_) |
 /_/    \_\__|_|\__,_|___/ |____/|_|\___/|_|_| |_|_| \___/

        `-:-.   ,-;"`-:-.   ,-;"`-:-.   ,-;"`-:-.   ,-;"
        `=`,'=/     `=`,'=/     `=`,'=/     `=`,'=/
            y==/        y==/        y==/        y==/
        ,=,-<=`.    ,=,-<=`.    ,=,-<=`.    ,=,-<=`.
        ,-'-'   `-=_,-'-'   `-=_,-'-'   `-=_,-'-'   `-=_

    '''
    description_text = '''{}
     Manage datasets on the Hugging Face Hub - upload, download, list and remove datasets.
    '''.format(logo)
    parser = argparse.ArgumentParser(description=description_text, formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    

    upload_parser = subparsers.add_parser('upload', help='Upload dataset to Hugging Face Hub')
    upload_parser.add_argument('-i', type=str, help='Path to the local dataset', required=True)
    upload_parser.add_argument('-r', type=str, help='Repository name for upload (format: username/repo_name). Default is the dataset folder name', default=None)
    upload_parser.add_argument('-p', type=bool, help='Make dataset public (default: False)', default=False)
    
    list_parser = subparsers.add_parser('list', help='List available datasets on Hugging Face Hub')
    list_parser.add_argument('-u', type=str, help='Hugging Face username', default="ATLASBIOINFO")
    list_parser.add_argument('-f', type=str, help='Filter datasets by keyword (case-insensitive)', default=None)

    remove_parser = subparsers.add_parser('remove', help='Remove dataset from Hugging Face Hub')
    remove_parser.add_argument('repo_name', type=str, help='Repository name to remove (format: username/repo_name)', required=True)
    remove_parser.add_argument('-f', type=bool, help='Force deletion without confirmation', default=False)
    
    download_parser = subparsers.add_parser('download', help='Download dataset from Hugging Face Hub')
    download_parser.add_argument('repo_name', type=str, help='Repository name to download (format: username/repo_name)')
    download_parser.add_argument('-o', type=str, help='Output directory path', default="./")

    check_parser = subparsers.add_parser('check', help='Check dataset statistics from Hugging Face Hub')
    check_parser.add_argument('repo_name', type=str, help='Repository name to check (format: username/repo_name)')

    args = parser.parse_args()

    
    if args.command == 'upload':
        upload_dataset(args.i, args.r, args.p)
    elif args.command == 'list':
        list_datasets(args.u, args.f)
    elif args.command == 'remove':
        remove_dataset(args.r, args.f)
    elif args.command == 'download':
        download_dataset(args.repo_name, args.o)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
