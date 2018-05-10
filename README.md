## YobiUtils - app_ExtractVidSamples.py [>=Python 3.4.x]

#### Description
This app can be used to generate samples of video files contained within a folder.  
Here are the details on how it functions:  

1) Lists all the files within a folder (parsing the sub-folders recursively)
2) To figure out potential video files, it uses mediainfo to get duration of a file
   [This step is not 100% reliable, since files like .db also end up giving a value for duration]
3) Attempt to extract a sample from the video file, with the following consideration:
    - Duration of extract can range from 30 seconds to 180 seconds (3 minutes)
    - Start point of the extract is chosen randomly somewhere within the video.
    - The extracted sample is designed to always start on a key-frame of the video [Might change in the future]
    - All the channels in the media file (video, audio, and subtitles) are exported without re-encoding)
    - Output filenames are uniquely generated based upon the path of a file

#### Setup

pip install -r requirements.txt


#### Usage
```python3
python app_ExtractVidSamples.py <input_folder> <output_folder>
```

##### NOTE:
- <output_folder> should lie outside of <input_folder>
- Ensure both <output_folder> and <input_folder> already exist
