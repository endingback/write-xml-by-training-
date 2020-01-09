from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from lxml import etree
import codecs
XML_EXT = '.xml'
ENCODE_METHOD = 'utf-8'
class PascalVocWriter:
    #writer = PascalVocWriter('test2',file, img.size, labels, boxes)
    def __init__(self, foldername, filename, imgSize, labels, boxes):
        self.foldername = foldername
        self.filename = filename
        self.imgSize = imgSize
        self.boxlist = []
        self.localImgPath = '/home/shijue/python_cv2/{}/{}'.format(foldername,filename)
        self.verified = False
        self.labels = labels
        self.boxes = boxes
        self.databaseSrc = 'Unknown'
    def prettify(self, elem):
        """
            Return a pretty-printed XML string for the Element.
        """
        rough_string = ElementTree.tostring(elem, 'utf8')
        root = etree.fromstring(rough_string)
        return etree.tostring(root, pretty_print=True, encoding=ENCODE_METHOD).replace("  ".encode(), "\t".encode())
        # minidom does not support UTF-8
        # '''reparsed = minidom.parseString(rough_string)
        # return reparsed.toprettyxml(indent="\t", encoding=ENCODE_METHOD)'''

    def genXML(self):
        """
            Return XML root
        """
        # Check conditions
        if self.filename is None or \
                self.foldername is None or \
                self.imgSize is None:
            return None

        top = Element('annotation')
        if self.verified:
            top.set('verified', 'yes')

        folder = SubElement(top, 'folder')
        folder.text = self.foldername

        filename = SubElement(top, 'filename')
        filename.text = self.filename

        if self.localImgPath is not None:
            localImgPath = SubElement(top, 'path')
            localImgPath.text = self.localImgPath
        source = SubElement(top, 'source')
        database = SubElement(source, 'database')
        database.text = self.databaseSrc
        size_part = SubElement(top, 'size')
        width = SubElement(size_part, 'width')
        height = SubElement(size_part, 'height')
        depth = SubElement(size_part, 'depth')
        width.text = str(self.imgSize[0])
        height.text = str(self.imgSize[1])
        depth.text = '3'
        segmented = SubElement(top, 'segmented')
        segmented.text = '0'
        return top

    def appendObjects(self, top):
        for each_object in range(len(self.labels)):
            object_item = SubElement(top, 'object')
            name = SubElement(object_item, 'name')
            name.text = self.labels[each_object]
            print(self.labels,"labels")
            print(name.text, "name")
            pose = SubElement(object_item, 'pose')
            pose.text = "Unspecified"
            truncated = SubElement(object_item, 'truncated')
            # if int(float(each_object['ymax'])) == int(float(self.imgSize[0])) or (int(float(each_object['ymin']))== 1):
            #     truncated.text = "1" # max == height or min
            # elif (int(float(each_object['xmax']))==int(float(self.imgSize[1]))) or (int(float(each_object['xmin']))== 1):
            #     truncated.text = "1" # max == width or min
            # else:
            truncated.text = "0"
            difficult = SubElement(object_item, 'difficult')
            difficult.text = "0"
            bndbox = SubElement(object_item, 'bndbox')
            xmin = SubElement(bndbox, 'xmin')
            xmin.text = str(int(self.boxes[each_object][0]))
            ymin = SubElement(bndbox, 'ymin')
            ymin.text = str(int(self.boxes[each_object][1]))
            xmax = SubElement(bndbox, 'xmax')
            xmax.text = str(int(self.boxes[each_object][2]))
            ymax = SubElement(bndbox, 'ymax')
            ymax.text = str(int(self.boxes[each_object][3]))

    def save(self, targetFile=None):
        root = self.genXML()
        self.appendObjects(root)
        out_file = None
        if targetFile is None:
            file = self.filename.split('.')[0]
            #写入当前xml文件夹中
            out_file = codecs.open(
            '/home/shijue/mmdetection/demo_results/xml/' + file + XML_EXT, 'w', encoding=ENCODE_METHOD)
            #写入labelImage对应的xml文件中
            # xml_file = codecs.open(
            # '/media/shijue/刘嘉豪/5_无人机数据/labelImage/' + file + XML_EXT, 'w', encoding=ENCODE_METHOD)
        else:
            out_file = codecs.open(targetFile, 'w', encoding=ENCODE_METHOD)
        prettifyResult = self.prettify(root)
        # xml_file.write(prettifyResult.decode('utf8'))
        # xml_file.close()
        out_file.write(prettifyResult.decode('utf8'))
        out_file.close()