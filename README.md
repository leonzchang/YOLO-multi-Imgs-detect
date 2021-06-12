# YOLO-multi-Imgs-detect
This is for [AlexeyAB/darknet](https://github.com/AlexeyAB/darknet) repository to predict multiple images and save results.

## Requirements
```
pip install -r requirements.txt
```

## Predict Images
```
ImgDetect.py [-h] -i INPUT -o OUTPUT -ds DATA_SETTING -cfg CONFIGURATION -w WEIGHT (-th THRESHOLD)

optional arguments:
  -h, --help          show this help message and exit
  -i INPUT            enter input path of images
  -o OUTPUT           enter save path of result images
  -ds DATA_SETTING    enter path of obj.data file
  -cfg CONFIGURATION  enter path of cfg-file
  -w WEIGHT           enter path of weight file
  -th THRESHOLD       enter threshold, default value is 0.25

```

NOTE:You should move ImgDetect.py to darknet folder before using

```
python imageDetect.py -i imgs_folder -o results_folder -ds data/obj.data -w backup/yolov4-custom_best.weights -cfg cfg/yolov4-custom.cfg (-th 0.3)
```



