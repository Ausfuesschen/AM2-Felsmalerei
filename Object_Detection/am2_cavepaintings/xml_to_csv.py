
# Verfasser: Dat Tran (https://github.com/datitran/raccoon_dataset/tree/e7c272aeb5f62ec575640ed6b4d8de9bf32e84bd)

import os
import glob
import pandas as pd
import tensorflow as tf
import xml.etree.ElementTree as ET

flags = tf.app.flags
flags.DEFINE_string('annotations_folder', '', 'Relative path to the annotations folder (train or test)')
flags.DEFINE_string('output_csv', '', 'Output file name')
FLAGS = flags.FLAGS

def xml_to_csv():
    image_path = os.path.join(os.getcwd(), FLAGS.annotations_folder)

    xml_list = []
    for xml_file in glob.glob(image_path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    xml_df.to_csv(FLAGS.output_csv, index=None)
    print('Successfully converted xml to csv.')


xml_to_csv()