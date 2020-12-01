# YOLO-multi-Imgs-detect
This is for [AlexeyAB/darknet](https://github.com/AlexeyAB/darknet) repository to predict multiple images and save results.




## Requirements
```
pip install -r requirements.txt
```


## Predict Images

```
python imageDetect.py -i mydata -o results -ds PVC/color/obj.data -w PVC/color/yolov4-custom_best.weights -cfg PVC/color/yolov4-custom.cfg
```
```
ImgDetect.py [-h] -i INPUT -o OUTPUT -ds data-setting -cfg CONFIGURATION -w WEIGHT

optional arguments:
  -h, --help          show this help message and exit
  -i INPUT            enter input path of images
  -o OUTPUT           enter save path of result images
  -ds data-setting    enter path of obj.data file
  -cfg CONFIGURATION  enter path of cfg-file
  -w WEIGHT           enter path of weight file

```



