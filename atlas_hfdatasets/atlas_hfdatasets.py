import logging, argparse,os,sys

try:
    from src.core_functions import login_to_hub, get_username, remove_dataset, download_dataset,  create_dataset
    from src.upload import upload_dataset
    from src.check import check_dataset
    from src.list import list_datasets
    from src.rename import rename_dataset
except ImportError:
    from atlas_hfdatasets.src.core_functions import login_to_hub, get_username, remove_dataset, download_dataset, create_dataset
    from atlas_hfdatasets.src.upload import upload_dataset
    from atlas_hfdatasets.src.check import check_dataset
    from atlas_hfdatasets.src.list import list_datasets
    from atlas_hfdatasets.src.rename import rename_dataset
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')

def main():
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

    init_parser = subparsers.add_parser('init', help='Initialize and login to Hugging Face Hub')

    create_parser = subparsers.add_parser('create', help='Create a new empty dataset repository on Hugging Face Hub')
    create_parser.add_argument('repo_name', type=str, help='Repository name to create (format: username/repo_name)')
    create_parser.add_argument('-p', type=bool, help='Make dataset public (default: False)', default=False)

    list_parser = subparsers.add_parser('list', help='List available datasets on Hugging Face Hub')
    list_parser.add_argument('-f', type=str, help='Filter datasets by keyword (case-insensitive)', default=None)

    download_parser = subparsers.add_parser('download', help='Download dataset from Hugging Face Hub')
    download_parser.add_argument('repo_name', type=str, help='Repository name to download (format: username/repo_name)')
    download_parser.add_argument('-o', type=str, help='Output directory path', default="./")

    upload_parser = subparsers.add_parser('upload', help='Upload dataset to Hugging Face Hub')
    upload_parser.add_argument('dataset_pattern', type=str, help='Dataset pattern to match datasets')
    upload_parser.add_argument('repo_name', type=str, help='Repository name for upload (format: username/repo_name). Default is the dataset folder name', default=None)
    upload_parser.add_argument('-p', type=bool, help='Make dataset public (default: False)', default=False)
    
    remove_parser = subparsers.add_parser('remove', help='Remove dataset from Hugging Face Hub')
    remove_parser.add_argument('repo_name', type=str, help='Repository name to remove (format: username/repo_name)')
    remove_parser.add_argument('-f', action='store_true', help='Force deletion without confirmation')
    
    check_parser = subparsers.add_parser('check', help='Check dataset statistics from Hugging Face Hub')
    check_parser.add_argument('repo_name', type=str, help='Repository name to check (format: username/repo_name)')

    rename_parser = subparsers.add_parser('rename', help='Rename dataset on Hugging Face Hub')
    rename_parser.add_argument('repo_name', type=str, help='Repository name to rename (format: username/repo_name)')
    rename_parser.add_argument('new_repo_name', type=str, help='New repository name (format: username/new_repo_name)')

    args = parser.parse_args()

    command_handlers = {
        'upload': lambda: upload_dataset(args.dataset_pattern, args.repo_name, args.p),
        'list': lambda: list_datasets(args.f, username),
        'remove': lambda: remove_dataset(args.repo_name, args.f),
        'download': lambda: download_dataset(args.repo_name, args.o),
        'check': lambda: check_dataset(args.repo_name),
        'create': lambda: create_dataset(args.repo_name, args.p),
        'rename': lambda: rename_dataset(args.repo_name, args.new_repo_name)
    }

    if args.command == 'init':
        login_to_hub()
    else:
        try:
            username = get_username()
        except:
            logging.error("Please login first by running 'atlas_hgdatasets init'")
            sys.exit(1)
        if args.command in command_handlers:
            command_handlers[args.command]()
        else:
            parser.print_help()

if __name__ == "__main__":
    main()
