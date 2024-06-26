# DeepFace®
DeepFace® is a Neural network system designed to swap multiple faces in videos with impressive accuracy.
In short, DeepFace® deepfake tool that allows users to create high-quality face swaps using deep learning techniques.

It offers a user-friendly interface and supports various deep learning models.


Take a video and replace the face in it with a face of your choice.
You only need one image of the desired face. No dataset, no training.

![DeepFace](https://raw.githubusercontent.com/skytells-research/DeepFace/main/assets/Deepface.png)


## Installation

Clone Repository

```sh
git clone https://github.com/skytells-research/deepface
```


Install dependencies
We highly recommend to work with a venv or conda to avoid issues.

```sh
pip install -r requirements.txt
```

You should be able to run deepface using python run.py command. 

Keep in mind that while running the program for first time, it will download some models which can take time depending on your network connection.

## Setup
Keep in mind that the installation needs technical skills and is not for beginners.

[Basic](https://github.com/skytells-research/DeepFace/blob/main/docs/setup.md) - It is more likely to work on your computer, but will be quite slow

[Acceleration](https://github.com/skytells-research/DeepFace/blob/main/docs/Acceleration.md) - Unleash the full potential of your CPU and GPU

## Usage
Start the program with arguments:
```sh
python run.py 
```
Done.


For advanced usage:

```sh
python run.py [options]
-h, --help                                                                 show this help message and exit
-s SOURCE_PATH, --source SOURCE_PATH                                       select an source image
-t TARGET_PATH, --target TARGET_PATH                                       select an target image or video
-o OUTPUT_PATH, --output OUTPUT_PATH                                       select output file or directory
--frame-processor FRAME_PROCESSOR [FRAME_PROCESSOR ...]                    frame processors (choices: face_swapper, face_enhancer, ...)
--keep-fps                                                                 keep target fps
--keep-frames                                                              keep temporary frames
--skip-audio                                                               skip target audio
--many-faces                                                               process every face
--reference-face-position REFERENCE_FACE_POSITION                          position of the reference face
--reference-frame-number REFERENCE_FRAME_NUMBER                            number of the reference frame
--similar-face-distance SIMILAR_FACE_DISTANCE                              face distance used for recognition
--temp-frame-format {jpg,png}                                              image format used for frame extraction
--temp-frame-quality [0-100]                                               image quality used for frame extraction
--output-video-encoder {libx264,libx265,libvpx-vp9,h264_nvenc,hevc_nvenc}  encoder used for the output video
--output-video-quality [0-100]                                             quality used for the output video
--max-memory MAX_MEMORY                                                    maximum amount of RAM in GB
--execution-provider {cpu} [{cpu} ...]                                     available execution provider (choices: cpu, ...)
--execution-threads EXECUTION_THREADS                                      number of execution threads
-v, --version                                                              show program's version number and exit
```

![DeepFace](https://raw.githubusercontent.com/skytells-research/DeepFace/main/assets/screenshot.png)


Headless
Using the `-s/--source`, `-t/--target` and `-o/--output` argument will run the program in headless mode.

## Disclaimer
This software is designed to contribute positively to the AI-generated media industry, assisting artists with tasks like character animation and models for clothing, We are aware of the potential ethical issues and have implemented measures to prevent the software from being used for inappropriate content, such as nudity.

* Users are expected to follow local laws and use the software responsibly. 
* If using real faces, get consent and clearly label deepfakes when sharing. 
* The developers aren't liable for user actions.

## Licenses
Our software uses a lot of third party libraries as well pre-trained models. 
The users should keep in mind that these third party components have their own license and terms, therefore our license is not being applied.


## Credits

- [deepinsight](https://github.com/deepinsight) for their [insightface](https://github.com/deepinsight/insightface) project which provided a well-made library and models.
