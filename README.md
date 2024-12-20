# Atlas_HFDatasets

A command-line tool to manage your datasets on the Hugging Face Hub - upload, download, list, check and remove datasets with ease.


## Prerequisites

- Python 3.7 or higher

## Installation

Install the package via pip:

```bash
pip install atlas_hfdatasets
```

## Usage

Before using the tool, initialise your Hugging Face credentials:

```bash
atlas_hfdatasets init
```

### Commands

- **Upload a dataset**
  ```bash
  atlas_hfdatasets upload /path/to/dataset [-n username/repo_name] [-p True/False]
  ```
  Options:
  - `-n`: Repository name (format: username/repo_name). Defaults to dataset folder name
  - `-p`: Make dataset public (default: False)

- **List your datasets**
  ```bash
  atlas_hfdatasets list [-f keyword]
  ```
  Options:
  - `-f`: Filter datasets by keyword (case-insensitive)

- **Remove a dataset**
  ```bash
  atlas_hfdatasets remove username/repo_name [-f True/False]
  ```
  Options:
  - `-f`: Force deletion without confirmation (default: False)

- **Download a dataset**
  ```bash
  atlas_hfdatasets download username/repo_name [-o output_directory]
  ```
  Options:
  - `-o`: Output directory path (default: current directory)

- **Check dataset statistics**
  ```bash
  atlas_hfdatasets check username/repo_name
  ```

## Requirements

- Python ≥ 3.7
- huggingface-hub
- datasets

## Licence

This project is licensed under the MIT Licence - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
```
