# File Splitter

This repository provides a file splitting program that is designed to split large files into smaller chunks. The program monitors a specified directory for new files and splits them based on the specified criteria. It is particularly useful when dealing with files that are too large to be efficiently processed by consuming applications.

## Features

- Monitors a directory for new files and automatically splits them into smaller files.
- Allows configuration of the splitting criteria, such as the maximum number of lines per split file.
- Supports various file extensions for splitting.
- Provides error handling and logging for monitoring and splitting operations.

## Requirements

- Python 3.6 or above
- `yaml` module

## Getting Started

1. Clone this repository to your local machine.
2. Install the required dependencies by running the following command:

`pip install pyyaml`

3. Update the `testsplitmd.yaml` configuration file with the desired input and output directories, line limit, and file extensions.
4. Run the program using the following command:

`python file_splitter.py`

5. The program will start monitoring the input directory for new files. Once a new file is detected, it will be split into smaller files based on the specified criteria and saved in the output directory.
6. You can customize the program by modifying the configuration file and adjusting the splitting criteria as per your requirements.

## Configuration

The program uses a YAML configuration file (`testsplitmd.yaml`) to specify the following parameters:

- `indir`: The input directory where new files are received.
- `outdir`: The output directory where the split files will be saved.
- `lineLimit`: The maximum number of lines per split file.
- `extension`: A list of file extensions to consider for splitting.

Ensure that you provide valid and accessible directory paths and extensions in the configuration file.

## Contributing

Contributions to enhance the functionality, performance, or usability of this file splitting program are welcome. If you would like to contribute, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make the necessary code changes.
4. Write tests to ensure code correctness, if applicable.
5. Commit your changes and push them to your forked repository.
6. Submit a pull request to the main repository for review and consideration.

## License

This project is licensed under the [MIT License](LICENSE).
