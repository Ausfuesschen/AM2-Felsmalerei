# AM2-Felsmalerei
Arbeitsgruppe von: Alexander Schroeder, Kristian Svane, Anja Wodzinski 


## Image Classification (TensorFlow)
... 


## Object Detection (Anja)
Training of a neural network (inception_v2 architecture) using TensorFlow Object Detection API.  

### Tensorflow Installation
* Python 3 (up to 3.6.5) required
* TensorFlow 1.8.0 (installation instructions: https://www.tensorflow.org/install/)
* Dependencies for TF Object Detection API (installation instructions: https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md)
* Helpful tutorial: https://towardsdatascience.com/how-to-train-your-own-object-detector-with-tensorflows-object-detector-api-bec72ecfe1d9

#### In *every new terminal:* add *TF-slim* to PATH variables! (API for training and evaluating models)
In *TensorFlow\models\research*: 
```
SET PYTHONPATH=%cd%;%cd%\slim 
echo %PYTHONPATH%
```

### Dataset preparation
* RGB image (jpg/png)
  image 0-9 = animal
  image 10-19 = man
  image 20-29 = text
  image 30-39 = woman
* List of bounding boxes (xmin, ymin, xmax, ymax)  -> XML

### Creating Bounding Boxes 
* Tool: **LabelImg**  -> create bounding boxes stored in **xml** files
  * Library: https://github.com/tzutalin/labelImg
  * Download prebuilt binary: https://tzutalin.github.io/labelImg/
  
### Convert Data from XML to CSV
* Script: xml_to_csv.py (by Dat Tran)
  * Source: https://github.com/datitran/raccoon_dataset/blob/e7c272aeb5f62ec575640ed6b4d8de9bf32e84bd/xml_to_csv.py
  * Alternative: Script in TensorFlow\models\research\object_detection\dataset_tools

#### Convert Training data XML 
```
python xml_to_csv.py 
--annotations_folder=training\annotations 
--output_csv=training\cavepaintings_labels_train.csv
```

#### Convert Testing data xml
```
python xml_to_csv.py 
--annotations_folder=testing\annotations 
--output_csv=testing\cavepaintings_labels_test.csv
```

### Create Label Map for TFRecord Files
* Create **label map** corresponding to TFRecord files dataset which contains IDs corresponding to labels 
* Example:https://github.com/tensorflow/models/tree/master/research/object_detection/data

### Generate TFRecords Files
* TFRecord = TensorFlow's standard file format 
* Input pipeline to feed TF program with our data 
* File takes list of filenames, creates a queue, reads and decodes the data 
* clone directory tensorflow\models from Github: https://github.com/tensorflow/models 

#### Training data
In *C:\Users\Computer\Documents\TensorFlow\am2_cavepaintings\training*: 
```
python ..\generate_tfrecord.py 
--csv_input=cavepaintings_labels_train.csv 
--output_path=train.record
```

#### Testing data
In *C:\Users\Computer\Documents\TensorFlow\am2_cavepaintings\testing*: 
```
python ..\generate_tfrecord.py 
--csv_input=cavepaintings_labels_test.csv 
--output_path=test.record
```

### Download pretrained model
* Principle: Transfer learning
* Download the pretrained model, so that it doesn't have to start from scratch every time
* Source: http://download.tensorflow.org/models/object_detection/ssd_inception_v2_coco_2017_11_17.zip

#### Edit Coco Config File Paths
In *models\model\ssd_inception_v2_coco.config*: 
* search for "path" and edit path (search for # PATH_TO_BE_CONFIGURED)
* adjust number of training steps (here: 200 (needs about 2h on my pc with Intel i5 and 8GB Ram) ; better: 200.000)
* change "num_classes" from 90 to 4 (man, woman, animal, text) 

### Training Process
In *C:\Users\Computer\Documents\TensorFlow\models\research*: 
```
python object_detection\train.py 
--logtostderr 
--pipeline_config_path=C:\\Users\\Computer\\Documents\\TensorFlow\\am2_cavepaintings\\models\\model\\ssd_inception_v2_coco.config 
--train_dir=C:\\Users\\Computer\\Documents\\TensorFlow\\am2_cavepaintings\\models\\model\\train\
```

### Testing Process  
Can be done parallel to training. 
In *C:\Users\Computer\Documents\TensorFlow\models\research*: 
```
python object_detection\eval.py --logtostderr --pipeline_config_path=C:\\Users\\Computer\\Documents\\TensorFlow\\am2_cavepaintings\\models\model\\ssd_inception_v2_coco.config --checkpoint_dir=C:\\Users\\Computer\\Documents\\TensorFlow\\am2_cavepaintings\\models\\model\\train\ --eval_dir=C:\\Users\\Computer\\Documents\\TensorFlow\\am2_cavepaintings\\models\\model\\eval\
```

### Montoring progress on Tensorboard 
Can be done parallel to training and testing. 
In *C:\Users\Computer\Documents\TensorFlow\models\research*: 
```
tensorboard --logdir=C:\\Users\\Computer\\Documents\\TensorFlow\\am2_cavepaintings\\models\model
```

### Freeze Graph
... 

### Our current state (26.07.18)
* Frozen graph: Object_Detection\am2_cavepaintings\output\frozen_interference_graph.pb
* Screenshot folder: Object_Detection\screenshots
* Output folder: Object_Detection\am2_cavepaintings\output\
* Fix evaluation error (see screenshot in output folder: \Object_Detection\screenshots\errors\evaluation_process_error.jpg)

### Files 
#### Own files
* Readme.md 
* label_map_pbtxt

#### Modified files
* *models\model\ssd_inception_v2_coco.config*: contains data for training 

#### Generated files
... 

#### Files of Dat Tran
* xml_to_csv.py: converts files in xml format to files in csv format
