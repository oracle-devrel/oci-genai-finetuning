# oci-genai-finetuning

[![License: UPL](https://img.shields.io/badge/license-UPL-green)](https://img.shields.io/badge/license-UPL-green) [![Quality gate](https://sonarcloud.io/api/project_badges/quality_gate?project=oracle-devrel_oci-genai-finetuning)](https://sonarcloud.io/dashboard?id=oracle-devrel_oci-genai-finetuning)

# OCI Language and Batch Translation 

## Overview of the service

This is an overview of what Oracle Cloud Infrastructure Vision (a.k.a. OCI Vision) is, what it can provide, and how it can be used to your advantage as a company or individual trying to work with Artificial Intelligence.

Of course, the domain we're going to observe is specifically going to focus on Computer Vision, a branch of Artificial Intelligence, that aims to use visual data to automate, or improve the quality of an application.

OCI Vision is a versatile service that focuses on this. We (the users) can access these services in the following ways:
Generative AI Service

Unlock the power of generative AI models equipped with advanced language comprehension for building the next generation of enterprise applications. Oracle Cloud Infrastructure (OCI) Generative AI is a fully managed service available via API to seamlessly integrate these versatile language models into a wide range of use cases, including writing assistance, summarization, and chat.

- Using an OCI SDK: seamless interaction with your favorite programming language, without needing to create your own custom implementation / framework.
- Using the OCI Console: easy-to-use, browser-based interface, by accessing your OCI account and using the services with the web interface provided by Oracle.
- Using the OCI Command-Line Interface (CLI): Quick access and full functionality without programming. The CLI is a package that allows you to use a terminal to operate with OCI.
- Using a RESTful API: Maximum functionality, requires programming expertise. (through requests)

The capabilities of OCI Vision can be divided into two:

- Document AI, or document processing: focuses on extracting or processing data from documents (usually readable)
- Image AI: focuses on detecting elements of an image, like objects, segments of the image...

These are some of the capabilities we can find in OCI Vision:

- Object Detection: Identify objects like people, cars, and trees in images, returning bounding box coordinates (meaning, a rectangle of varying size, depending on the object). (Image AI)
- Image Classification: categorize objects in images. (Image AI)
- Optical Character Recognition (OCR): Locate and digitize text in images. (Document AI)
- Face Recognition: detecting faces in images and key points in faces, which can be later used to process the face's mood, position... (Image AI)

If you're unhappy with the set of elements being recognized in OCI Vision, or you're trying to detect something in images that is uncommon / not real (e.g. a character in a Disney movie, or a new species of animal), you can also create your own *Custom Model*:

- Custom Object Detection: build models to detect custom objects with bounding box coordinates.
- Custom Image Classification: create models to identify specific objects and scene-based features.

### Document AI

> **Note**: Document AI features are available until January 1, 2024. Post that, they will be available in another OCI service called OCI Document Understanding.

There are lots of things that we can extract from a document: information from receipts (prices, dates, employees...), tabular data (if the document has tables/spreadsheets on it), or simply text contained in a document.

All of this is specially useful for retail or HR companies, to manage their inventories, transactions, and manage their resources and activities more efficiently. It can also generate searchable, summarized PDFs from all this data, uploaded to the Cloud and accessible anywhere.

### Supported File Formats

Here's a list of supported file formats:

- JPG
- PNG
- JPEG
- PDF
- TIFF (great for iOS enthusiasts)

Oracle Cloud Infrastructure Vision is a robust, flexible and cost-effective service for Computer Vision tasks. Oh, and extremely speedy!

Whether you're dealing with images or documents, OCI Vision has all the tools you need, so make sure to give them a try.

## Introduction

This project teaches you how to develop an AI-infused application with OCI Vision. For this project, we will be using OCI's Python SDK to invoke the OCI Vision service and get results on detections. We have prepared several scripts, which can be found in the `scripts` folder, to make the appropriate calls to the service, regarding Image Classification and Object Detection.

Finally, this demo also has an implementation of Object Detection with `ThreadPools`, to automate this process and allow you to process whole video files by separating the video into frames and calling the Object Detection endpoint for each frame; then, recomposing all frames into an output video file.

## 0. Prerequisites and setup

- Oracle Cloud Infrastructure (OCI) Account
- [Oracle Cloud Infrastructure Documentation - Vision](https://docs.oracle.com/en-us/iaas/Content/vision/using/home.htm)
- [Oracle Cloud Infrastructure (OCI) Generative AI Service SDK - Oracle Cloud Infrastructure Python SDK](https://pypi.org/project/oci/)
- [Python 3.10](https://www.python.org/downloads/release/python-3100/)
- [Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
- [OCI SDK](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm)

Follow these links below to generate a config file and a key pair in your ~/.oci directory:

- [SDK Config](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm)
- [API Signing Key](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.htm)
- [SDK CLI Installation](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm#configfile)

After completion, you should have following 2 things in your ~/.oci directory:

- A config file(where key file point to private key:key_file=~/.oci/oci_api_key.pem)
- A key pair named oci_api_key.pem and oci_api_key_public.pem
- Now make sure you change the reference of key file in config file (where key file point to private key:key_file=/YOUR_DIR_TO_KEY_FILE/oci_api_key.pem)

> **Note**: if you have saved your OCI config file somewhere else, make sure to reference this location in `scripts/video_processing.py`, line 156:

```python
config = oci.config.from_file(
             oci.config.DEFAULT_LOCATION,
             (config_profile if config_profile else oci.config.DEFAULT_PROFILE),
        )
```

And change it to:

```python
config = oci.config.from_file(
             "<NEW_LOCATION>",
             (config_profile if config_profile else oci.config.DEFAULT_PROFILE),
        )
```

Finally, we install Python dependencies:

```sh
pip install -r requirements.txt
```

Then, we will create a Bucket in our OCI tenancy, and upload the pictures we want to analyze over there. This will ultimately depend on your use case, if you're trying to count the number of objects in an image (for traffic management), count people (for access management)... You will have to decide.

## 1. Create OCI Bucket

Let's create the Bucket:

1. Open the **Navigation** menu in the Oracle Cloud console and click **Storage**. Under **Object Storage & Archive Storage**, click **Buckets**.

2. On the **Buckets** page, select the compartment where you want to create the bucket from the **Compartment** drop-down list in the **List Scope** section. Make sure you are in the region where you want to create your bucket.

3. Click **Create Bucket**.

4. In the **Create Bucket** panel, specify the following:
    - **Bucket Name:** Enter a meaningful name for the bucket.
    - **Default Storage Tier:** Accept the default **Standard** storage tier. Use this tier for storing frequently accessed data that requires fast and immediate access. For infrequent access, choose the **Archive** storage tier.
    - **Encryption:** Accept the default **Encrypt using Oracle managed keys**.

5. Click **Create** to create the bucket.

  ![The completed Create Bucket panel is displayed.](./img/create-bucket-panel.png)

The new bucket is displayed on the **Buckets** page.

  ![The new bucket is displayed on the Buckets page.](./img/bucket-created.png)

## 1. (Optional) Running Image Classification with Object Storage

We will run `scripts/image_classification.py`, but before, we need to obtain some info from our OCI Bucket and replace it in our script, line 37:

![Information needed from bucket](./img/info_needed_bucket.PNG)

Then, we can just run the following command:

```bash
python image_classification.py
```

To run OCI Vision's image classification against that image. These results will be in JSON format.

## 2. (Optional) Running Object Detection with Object Storage

We will repeat the steps to obtain the information as in step 1 above:

![Information needed from bucket for Object Detection](./img/info_needed_bucket_object_detection.PNG)

Then we can proceed and run the following command:

```bash
python object_detection.py
```

And we'll obtain a JSON object detailing detections.

Optionally, you can uncomment the block starting in line 107, to visualize these results. Note that you must have the file locally and reference it in order to draw detections on top of the local image:

![Uncomment this code block](./img/codeblock_uncomment.PNG)

## 3. Batch processing any video with OCI Vision

We have prepared two different scripts for you:

- One script will generate an output MP4 file with results inserted into it.
- The other script will process the video frame-by-frame, process detections into a single `.json` file, but won't produce an output file. It's a way to learn how to invoke the service and aggregate results.

### Run Detector

```bash
python detector_video.py [-h] --video-file VIDEO_FILE [--model-id MODEL_ID] 
    [--output-frame-rate OUTPUT_FRAME_RATE] [--confidence-threshold CONFIDENCE_THRESHOLD] [-v]
```

For example, in my case, where I want only to draw objects above 80% model confidence, 30 frames per second (in my output video), and using the standard OCI Vision model (not a custom one), I would run:

```bash
python detector_video.py --video-file="H:/Downloads/my_video.mp4" --output-frame-rate="30" --confidence-threshold="80" -v
```

### Create Output Video (CPU-intensive)

```bash
python video_processer.py --file FILE_PATH
```

For example:

```bash
python video_processer.py --file="H:/Downloads/my_video.mp4" --mode="moderate"
```

## Demo

[OCI Vision Overview - Exploring the Service](https://www.youtube.com/watch?v=eyJm7OlaRBk&list=PLPIzp-E1msraY9To-BB-vVzPsK08s4tQD&index=4)

## Tutorial

Here’s an use case being solved with OCI Vision + Python:

[App Pattern: OCI Vision Customized Object Detector in Python](https://www.youtube.com/watch?v=B9EmMkqnoGQ&list=PLPIzp-E1msraY9To-BB-vVzPsK08s4tQD&index=2)

## Physical Architecture

![arch](./img/arch.PNG)

## Contributing

This project is open source.  Please submit your contributions by forking this repository and submitting a pull request!  Oracle appreciates any contributions that are made by the open source community.

## License

Copyright (c) 2022 Oracle and/or its affiliates.

Licensed under the Universal Permissive License (UPL), Version 1.0.

See [LICENSE](LICENSE) for more details.

ORACLE AND ITS AFFILIATES DO NOT PROVIDE ANY WARRANTY WHATSOEVER, EXPRESS OR IMPLIED, FOR ANY SOFTWARE, MATERIAL OR CONTENT OF ANY KIND CONTAINED OR PRODUCED WITHIN THIS REPOSITORY, AND IN PARTICULAR SPECIFICALLY DISCLAIM ANY AND ALL IMPLIED WARRANTIES OF TITLE, NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A PARTICULAR PURPOSE.  FURTHERMORE, ORACLE AND ITS AFFILIATES DO NOT REPRESENT THAT ANY CUSTOMARY SECURITY REVIEW HAS BEEN PERFORMED WITH RESPECT TO ANY SOFTWARE, MATERIAL OR CONTENT CONTAINED OR PRODUCED WITHIN THIS REPOSITORY. IN ADDITION, AND WITHOUT LIMITING THE FOREGOING, THIRD PARTIES MAY HAVE POSTED SOFTWARE, MATERIAL OR CONTENT TO THIS REPOSITORY WITHOUT ANY REVIEW. USE AT YOUR OWN RISK.
