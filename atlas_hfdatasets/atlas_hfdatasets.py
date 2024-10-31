import logging, argparse,os,sys
from cores.core_functions import login_to_hub, get_username, remove_dataset, list_datasets, upload_dataset, download_dataset, check_dataset
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

    list_parser = subparsers.add_parser('list', help='List available datasets on Hugging Face Hub')
    list_parser.add_argument('-f', type=str, help='Filter datasets by keyword (case-insensitive)', default=None)

    download_parser = subparsers.add_parser('download', help='Download dataset from Hugging Face Hub')
    download_parser.add_argument('repo_name', type=str, help='Repository name to download (format: username/repo_name)')
    download_parser.add_argument('-o', type=str, help='Output directory path', default="./")

    upload_parser = subparsers.add_parser('upload', help='Upload dataset to Hugging Face Hub')
    upload_parser.add_argument('dataset_path', type=str, help='Path to the local dataset')
    upload_parser.add_argument('-n', type=str, help='Repository name for upload (format: username/repo_name). Default is the dataset folder name', default=None)
    upload_parser.add_argument('-p', type=bool, help='Make dataset public (default: False)', default=False)
    
    remove_parser = subparsers.add_parser('remove', help='Remove dataset from Hugging Face Hub')
    remove_parser.add_argument('repo_name', type=str, help='Repository name to remove (format: username/repo_name)')
    remove_parser.add_argument('-f', type=bool, help='Force deletion without confirmation', default=False)
    
    check_parser = subparsers.add_parser('check', help='Check dataset statistics from Hugging Face Hub')
    check_parser.add_argument('repo_name', type=str, help='Repository name to check (format: username/repo_name)')

    args = parser.parse_args()


    if args.command == 'init':
        login_to_hub()
    else:
        try:
            username = get_username()
            if args.command == 'upload':
                upload_dataset(args.dataset_path, args.n, args.p)
            elif args.command == 'list':
                list_datasets(args.f, username)
            elif args.command == 'remove':
                remove_dataset(args.repo_name, args.f)
            elif args.command == 'download':
                download_dataset(args.repo_name, args.o)
            elif args.command == 'check':
                check_dataset(args.repo_name)
            else:
                parser.print_help()
        except:
            logging.error("Please login first by running 'atlas_hgdatasets init'")
            sys.exit(1)

if __name__ == "__main__":
    main()
