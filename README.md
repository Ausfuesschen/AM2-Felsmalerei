# AM2-Felsmalerei
Arbeitsgruppe von: Alexander Schroeder, Kristian Svane, Anja Wodzinski 

## Projektbeschreibung
Das vorliegeden Projekt setzt sich mit zwei verschiedenen Arten der Bilderkennung durch Machine Learning auseinander. Die erste Methode ist die Image Classification, welche Bilder mit einzelnen Objekten vorher definierten Klassen zuweisen kann. Die zweite Methode erweitert die erste Methode um die Object Detection. Damit lassen sich auf einem Bild mit mehreren Objekten die einzelnen Objekte bestimmen. Die ist besonders nützlich, da die Seiten mit den Figuren in der Theorie ohne Vorarbeit eingelesen werden können, dann die Objekte erkannt werden und zuletzt dann einer Klasse zugewiesen werden können. Allerdings erfordert die Object Detection einen signifikanteren Aufwand bei der Vorbereitung der Daten, da die Objekten in den Bildern zu Trainingszwecken alle einzelnd makiert werden müssen.
Die Unterschiede zwischen den Methoden werden in dem Bild (Classification_vs_Detection.jpeg) nochmal erläutert.

## Image Classification (TensorFlow / Mac OS)

### Vorbereitung und Installation
Die Basis für die Image Classification liefert das Beispielprojekt TensorFlow For Poets (https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/). Die Installation kann unter OS X auch nativ erfolgen, aber es empfiehlt sich eine Installation von Docker, die einen Linux Kernel in einem Container bereitstellt. So können mehrere Projekte mit unterschiedlichen Versionsanforderungen einfacher realisiert werden. Zudem ist der Austausch zwischen verschiedenen Computern und Betriebssystemen einfacher.

### Anpassung
Da in diesem Fall wir eine Unterscheidung zwischen verschiedenen Höhlenmalereien treffen wollen, werden die existieren Klassen ausgetauscht gegen die gewünschten eigenen Klassen. Des Weiteren wird statt dem MobileNet Neural Network, das weitaus effizientere Inception_v3 Model verwendet. Dieses braucht zwar für das Training mehr Zeit, allerdings kann dieses auch bei einer geringeren Anzahl an Trainingsdaten genauere Ergebnisse liefern.

### Benutzung
Zuerst wird mit folgenden Bash Befehl das Tensorboard gestartet, welches über den Browser abgerufen werden kann.

    tensorboard --logdir tf_files/training_summaries &
    
Danach kann über folgendene Befehle das Training gestartet werden. Dabei können die Parameter bei Bedarf noch angepasst werden. Weitere Parameter können der scripts.py entnommen werden.

    ARCHITECTURE="inception_v3"

    python -m scripts.retrain \
    --bottleneck_dir=tf_files/bottlenecks \
    --how_many_training_steps=2000 \
    --model_dir=tf_files/models/ \
    --summaries_dir=tf_files/training_summaries/"${ARCHITECTURE}" \
    --output_graph=tf_files/retrained_graph.pb \
    --output_labels=tf_files/retrained_labels.txt \
    --architecture="${ARCHITECTURE}" \
    --image_dir=tf_files/cave_paintings

Zuletzt kann das Model benutzt und getestet werden. Hier ist der Pfad zum Bild zu ersetzen.

    python -m scripts.label_image \
    --graph=tf_files/retrained_graph.pb  \
    --image=path/to/image.jpg



## Object Detection (TensorFlow / Windows 7)
Training of a neural network (inception_v2 architecture from the TensorFlow model zoo) using TensorFlow Object Detection API.  

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
Save the trained model as frozen TF Graph in order to test it in a Jupyter Notebook on new images.
```
python object_detection\export_inference_graph.py –input_type=image_tensor --pipeline_config_path=C:\\Users\\Computer\\Documents\\TensorFlow\\am2_cavepaintings\\models\model\\ssd_inception_v2_coco.config --trained_checkpoint_prefix=C:\\Users\\Computer\\Documents\\TensorFlow\\am2_cavepaintings\\models\\model\\train\model.ckpt-200 --output_directory=C:\\Users\\Computer\\Documents\\TensorFlow\\am2_cavepaintings\\output
```

### Testing model on new images
In order to test the model on new images, install the jupyter notebook library and replace the .ipynb file with the one on this git. Paths to files, used pretrained model, number of classes and names of images need to be adjusted afterwards. 
* Helpful tutorial: https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb

### Our current state (30.08.18)
* Frozen graph: Object_Detection\am2_cavepaintings\output\frozen_interference_graph.pb
* Screenshot folder: Object_Detection\screenshots
* Output folder: Object_Detection\am2_cavepaintings\output\

#### Own files
* Readme.md (part Object Detection)
* label_map_pbtxt

#### Modified files
* *models\model\ssd_inception_v2_coco.config*: contains data for training 
* *TensorFlow\models\research\object_detection\eval.py*: code added for logging details during evaluation process
* *am2_cavepaintings\object_detection_tutorial_cavepaintings.ipynb*: Jupyter Notebook file with Object Detection tutorial, modified to be used with our dataset. 

#### Files of Tran Dat
* xml_to_csv.py: converts files in xml format to files in csv format
