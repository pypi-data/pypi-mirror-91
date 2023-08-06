# storage-script

Script for uploading/downloading models to/from AWS S3 Cloud Storage

- [Installation](#installation)
- [Usage](#usage)

## Environment Variables

Please make sure to add the following variables in your environment

```
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export AWS_DEFAULT_REGION=
export AWS_S3_BUCKET_RASA_MODELS=
export AWS_ENDPOINT_URL=
```

## Requirements

* Local Python Installation
* [Boto3](https://pypi.org/project/boto3/)

## Installation
```
pip install git+https://github.tools.sap/dsx/storage-script.git
```

## Usage

```
rasa_storage [-h] [--version] {upload,download} 

    positional arguments:
    {upload,download}  Rasa Storage Commands
        upload           Uploads RASA models to AWS S3
        download         Downloads RASA models from AWS S3
    optional arguments:
    -h, --help         show this help message and exit
    --version, -v      Package Version
````

### Upload

```
rasa_storage upload [-h] --model MODEL [--folder FOLDER]
    -h, --help            show this help message and exit
    --model MODEL, -m MODEL
                            Relative path to the Model (.tar.gz file) (default:
                            None)
    
    optional arguments:
    --folder FOLDER, -f FOLDER
                            Optional: Folder Name where the model needs to be
                            saved in AWS S3 (default: master)
````

### Download

```
rasa_storage download [-h] --model MODEL [--folder FOLDER]

    -h, --help            show this help message and exit
    --model MODEL, -m MODEL
                            Model Name(.tar.gz file) (default: None)
    optional arguments:
    --folder FOLDER, -f FOLDER
                            Optional: Folder Name from where the model needs to be
                        downloaded (default: master)
```