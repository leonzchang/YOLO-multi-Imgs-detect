import argparse
import cv2
import os
import darknet

# enable GPU
os.environ["CUDA_VISIBLE_DEVICES"] = "0"


def detect_obj(img, network, metadata, threshold):
    '''
    load network configuration
    detect object
    '''
    frame_width = img.shape[0]
    frame_height = img.shape[1]
    frame_channel = img.shape[2]
    # opencv imread format is BGR yolo using RGB
    frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(
        frame_rgb, (frame_height, frame_width), interpolation=cv2.INTER_LINEAR)
    darknet_image = darknet.make_image(
        frame_height, frame_width, frame_channel)
    darknet.copy_image_from_bytes(darknet_image, frame_resized.tobytes())
    detections = darknet.detect_image(
        network, metadata, darknet_image, thresh=threshold)
    # free memory
    darknet.free_image(darknet_image)

    return detections  # return result [(cat., confidence,(x, y, w, h))]


def convertBack(x, y, w, h):
    '''
    get the coordinate of bounding box  
    '''
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax


def draw_defact(xmin, ymin, xmax, ymax, img, className):
    '''
    draw bounding box
    '''
    cv2.rectangle(img, (xmin, ymin),
                  (xmax, ymax), (10, 167, 255), 1)
    cv2.putText(img, className, (xmin, ymin),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10, 167, 255), 1, cv2.LINE_AA)
    return img


def image_detect(path, filename, network, metadata, threshold):
    '''
    detect targets in image 
    '''
    img = cv2.imread(path+'/'+filename)
    detect_result = detect_obj(img, network, metadata, threshold)
    for defect_unit in detect_result:
        xmin, ymin, xmax, ymax = convertBack(
            defect_unit[2][0], defect_unit[2][1], defect_unit[2][2], defect_unit[2][3])

        className = defect_unit[0].decode('utf-8')
        result_img = draw_defact(
            xmin, ymin, xmax, ymax, img, className)
    return result_img


def command():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', metavar=("INPUT"),
                        type=str, required=True, help='enter input path of images')
    parser.add_argument('-o', metavar=("OUTPUT"),
                        type=str, required=True, help='enter save path of result images')
    parser.add_argument('-ds', metavar=('DATA_SETTING'),
                        type=str, required=True, help="enter path of obj.data file")
    parser.add_argument('-cfg', metavar=('CONFIGURATION'),
                        type=str, required=True, help="enter path of cfg-file")
    parser.add_argument('-w', metavar=('WEIGHT'),
                        type=str, required=True, help='enter path of weight file')
    parser.add_argument('-th', metavar=('THRESHOLD'),
                        type=float, default=0.25,  help='enter threshold default value is 0.25')

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    # example: python ImgDetect.py -i mydata -o results -ds PVC/color/obj.data -w PVC/color/yolov4-custom_best.weights -cfg PVC/color/yolov4-custom.cfg
    args = command()

    # yolo config & weight file
    configPath = args.cfg
    weightPath = args.w
    metaPath = args.ds
    threshold = args.th

    # yolo setting
    # config_file (str) weights (str) GPU_id Batch_size
    network = darknet.load_net_custom(configPath.encode(
        "ascii"), weightPath.encode("ascii"), 0, 1)
    metadata = darknet.load_meta(metaPath.encode("ascii"))

    # setting input & output path
    input_path = args.i
    output_path = args.o

    # get all input imgs data
    imgs = os.listdir(input_path)

    print('process images......')
    for img in imgs:
        result_img = image_detect(
            input_path, img, network, metadata, threshold)
        cv2.imwrite(output_path+'/'+img, result_img)
    print('done.')
