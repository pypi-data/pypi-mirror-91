from copy import deepcopy
import re
import warnings
from lxml.etree import Element
from lxml import etree
from zipfile import ZipFile, ZIP_DEFLATED
from random import randint
from PIL import Image
import shlex
import mimetypes
import os.path


NAMESPACES = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
    'ct': 'http://schemas.openxmlformats.org/package/2006/content-types',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
}

CONTENT_TYPES_PARTS = (
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml',
)

CONTENT_TYPE_SETTINGS = 'application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml'


class MailMerge(object):
    def __init__(self, file, remove_empty_tables=False):
        self.file = file
        self.zip = ZipFile(file)
        self.parts = {}
        self.settings = None
        self._settings_info = None

        self.media = {}         # new images to add indexed by embed id,还有记录拓展名
        self.rels = None        # etree for relationships
        self._rels_info = None  # zi info block for rels
        self.RELS_NAMESPACES = {'ns': None, 'od': None}

        self.remove_empty_tables = remove_empty_tables

        try:
            content_types = etree.parse(self.zip.open('[Content_Types].xml'))
            for file in content_types.findall('{%(ct)s}Override' % NAMESPACES):
                type = file.attrib['ContentType' % NAMESPACES]
                if type in CONTENT_TYPES_PARTS:
                    zi, self.parts[zi] = self.__get_tree_of_file(file)
                elif type == CONTENT_TYPE_SETTINGS:
                    self._settings_info, self.settings = self.__get_tree_of_file(file)

            # get the rels for image mappings
            try:
                self._rels_info, self.rels = self.__get_tree_of_file('word/_rels/document.xml.rels')
                self.RELS_NAMESPACES['ns'] = self.rels.getroot().nsmap.get(None)
                self.RELS_NAMESPACES['od'] = self.rels.getroot().nsmap.get(None).replace('package', 'officeDocument')
            except:
                pass

            to_delete = []

            r = re.compile(r' MERGEFIELD +"?([^ ]+?)"? +(|\\\* MERGEFORMAT )', re.I)
            for part in self.parts.values():

                for parent in part.findall('.//{%(w)s}fldSimple/..' % NAMESPACES):
                    for idx, child in enumerate(parent):
                        if child.tag != '{%(w)s}fldSimple' % NAMESPACES:
                            continue
                        instr = child.attrib['{%(w)s}instr' % NAMESPACES]

                        name = self.__parse_instr(instr)
                        if name is None:
                            continue
                        parent[idx] = Element('MergeField', name=name)
                        # m = r.match(instr)
                        # if m is None:
                        #     continue
                        # parent[idx] = Element('MergeField', name=m.group(1))

                for parent in part.findall('.//{%(w)s}instrText/../..' % NAMESPACES):
                    children = list(parent)
                    fields = zip(
                        [children.index(e) for e in
                         parent.findall('{%(w)s}r/{%(w)s}fldChar[@{%(w)s}fldCharType="begin"]/..' % NAMESPACES)],
                        [children.index(e) for e in
                         parent.findall('{%(w)s}r/{%(w)s}fldChar[@{%(w)s}fldCharType="end"]/..' % NAMESPACES)]
                    )

                    for idx_begin, idx_end in fields:
                        # consolidate all instrText nodes between'begin' and 'end' into a single node
                        begin = children[idx_begin]
                        instr_elements = [e for e in
                                          begin.getparent().findall('{%(w)s}r/{%(w)s}instrText' % NAMESPACES)
                                          if idx_begin < children.index(e.getparent()) < idx_end]
                        if len(instr_elements) == 0:
                            continue

                        # set the text of the first instrText element to the concatenation
                        # of all the instrText element texts
                        instr_text = ''.join([e.text for e in instr_elements])
                        instr_elements[0].text = instr_text

                        # delete all instrText elements except the first
                        for instr in instr_elements[1:]:
                            instr.getparent().remove(instr)

                        name = self.__parse_instr(instr_text)
                        if name is None:
                            continue

                        parent[idx_begin] = Element('MergeField', name=name)
                        # m = r.match(instr_text)
                        # if m is None:
                        #     continue
                        # parent[idx_begin] = Element('MergeField', name=m.group(1))

                        # use this so we know *where* to put the replacement
                        instr_elements[0].tag = 'MergeText'
                        block = instr_elements[0].getparent()
                        # append the other tags in the w:r block too
                        parent[idx_begin].extend(list(block))

                        to_delete += [(parent, parent[i + 1])
                                      for i in range(idx_begin, idx_end)]

            for parent, child in to_delete:
                parent.remove(child)

            # Remove mail merge settings to avoid error messages when opening document in Winword
            if self.settings:
                settings_root = self.settings.getroot()
                mail_merge = settings_root.find('{%(w)s}mailMerge' % NAMESPACES)
                if mail_merge is not None:
                    settings_root.remove(mail_merge)
        except:
            self.zip.close()
            raise

    @classmethod
    def __parse_instr(cls, instr):
        args = shlex.split(instr, posix=False)
        if args[0] != 'MERGEFIELD':
            return None
        name = args[1]
        if name[0] == '"' and name[-1] == '"':
            name = name[1:-1]
        return name

    def __get_tree_of_file(self, file):
        # fn = file.attrib['PartName' % NAMESPACES].split('/', 1)[1]
        if isinstance(file, etree._Element):
            fn = file.get('PartName').split('/', 1)[1]
        else:
            fn = file
        zi = self.zip.getinfo(fn)
        return zi, etree.parse(self.zip.open(zi))

    def write(self, file):
        # Replace all remaining merge fields with empty values
        # Remove all remaining image with descr="delete"
        for field in self.get_merge_fields():
            self.merge(**{field: ''})

        # reservedIdList = []
        # parts = self.parts.values()
        # for part in parts:
        #     for image in part.findall('.//wp:docPr/..', namespaces=NAMESPACES):
        #         picNode = image.find('.//wp:docPr', namespaces=NAMESPACES)
        #         if "descr" not in picNode.attrib.keys() or picNode.attrib['descr'] != 'deletable':
        #             embed_node = image.find('.//a:blip', namespaces=NAMESPACES)
        #             if embed_node is not None:
        #                 embed_attr = embed_node.attrib.keys()[0]
        #                 imageId = embed_node.attrib[embed_attr]
        #                 if "rId" in imageId:
        #                     reservedIdList.append(imageId)
        # # Id get, all Ids.  then check if has not deletable image exists, then keep write the image to new file
        # regStr = r'<[^<]*Id="(rId\d+)"[^<]*Target="([^<]*)"/>'
        # r = re.compile(regStr)
        # with self.zip.open("word/_rels/document.xml.rels") as relFile:
        #     content = relFile.read().decode("utf8")
        # res = r.findall(content)
        # # keep rId,target as dict
        # idTarget = dict(res)
        # targetList = [idTarget[rId] for rId in reservedIdList]

        with ZipFile(file, 'w', ZIP_DEFLATED) as output:
            for zi in self.zip.filelist:
                zfname = zi.filename
                if zi in self.parts:
                    xml = etree.tostring(self.parts[zi].getroot(),encoding='utf-8')
                    # remove delete image's w:drawing xml block from document.xml
                    if zfname == "word/document.xml":
                        docContent = xml.decode('utf8')
                        reg = re.compile(r'<w:drawing>(?=.*descr).+?<\/w:drawing>')
                        # regex too hard…… so, use __reFun function add condition to remove
                        xml = reg.sub(self.__reFun, docContent)
                    output.writestr(zi.filename, xml)
                elif zi == self._settings_info:
                    xml = etree.tostring(self.settings.getroot())
                    output.writestr(zi.filename, xml)
                elif zi == self._rels_info:
                    xml = etree.tostring(self.rels.getroot())
                    output.writestr(zi.filename, xml)
                else:
                    # if zfname.endswith((".bmp", ".png", ".jpeg", ".jpg", ".gif", ".ico")) and zfname.split("word/")[-1] not in targetList:
                    #     # not reserved image, no need to write
                    #     pass
                    # else:
                    # 由于水印图片，就把所有图片保留，因为那个小占位图片不大3KB
                    output.writestr(zi.filename, self.zip.read(zi))
            # add new images to media folder is we have images merged
            for img_id_extension, img_data in self.media.items():
                arr = img_id_extension.split(':')
                output.writestr('word/media/{}.{}'.format(arr[0], arr[1]), img_data)

    def __reFun(self, obj):
        str = obj.group()
        if 'deletable' in str:
            return ''
        else:
            return str

    def get_merge_fields(self, parts=None):
        if not parts:
            parts = self.parts.values()
        fields = set()
        for part in parts:
            for mf in part.findall('.//MergeField'):
                fields.add(mf.attrib['name'])
        return fields

    def merge_templates(self, replacements, separator):
        """
        Duplicate template. Creates a copy of the template, does a merge, and separates them by a new paragraph, a new break or a new section break.
        separator must be :
        - page_break : Page Break.
        - column_break : Column Break. ONLY HAVE EFFECT IF DOCUMENT HAVE COLUMNS
        - textWrapping_break : Line Break.
        - continuous_section : Continuous section break. Begins the section on the next paragraph.
        - evenPage_section : evenPage section break. section begins on the next even-numbered page, leaving the next odd page blank if necessary.
        - nextColumn_section : nextColumn section break. section begins on the following column on the page. ONLY HAVE EFFECT IF DOCUMENT HAVE COLUMNS
        - nextPage_section : nextPage section break. section begins on the following page.
        - oddPage_section : oddPage section break. section begins on the next odd-numbered page, leaving the next even page blank if necessary.
        """

        # TYPE PARAM CONTROL AND SPLIT
        valid_separators = {'page_break', 'column_break', 'textWrapping_break', 'continuous_section',
                            'evenPage_section', 'nextColumn_section', 'nextPage_section', 'oddPage_section'}
        if not separator in valid_separators:
            raise ValueError("Invalid separator argument")
        type, sepClass = separator.split("_")

        # GET ROOT - WORK WITH DOCUMENT
        for part in self.parts.values():
            root = part.getroot()
            tag = root.tag
            if tag == '{%(w)s}ftr' % NAMESPACES or tag == '{%(w)s}hdr' % NAMESPACES:
                continue

            if sepClass == 'section':

                # FINDING FIRST SECTION OF THE DOCUMENT
                firstSection = root.find("w:body/w:p/w:pPr/w:sectPr", namespaces=NAMESPACES)
                if firstSection == None:
                    firstSection = root.find("w:body/w:sectPr", namespaces=NAMESPACES)

                # MODIFY TYPE ATTRIBUTE OF FIRST SECTION FOR MERGING
                nextPageSec = deepcopy(firstSection)
                for child in nextPageSec:
                    # Delete old type if exist
                    if child.tag == '{%(w)s}type' % NAMESPACES:
                        nextPageSec.remove(child)
                # Create new type (def parameter)
                newType = etree.SubElement(nextPageSec, '{%(w)s}type' % NAMESPACES)
                newType.set('{%(w)s}val' % NAMESPACES, type)

                # REPLACING FIRST SECTION
                secRoot = firstSection.getparent()
                secRoot.replace(firstSection, nextPageSec)

            # FINDING LAST SECTION OF THE DOCUMENT
            lastSection = root.find("w:body/w:sectPr", namespaces=NAMESPACES)

            # SAVING LAST SECTION
            mainSection = deepcopy(lastSection)
            lsecRoot = lastSection.getparent()
            lsecRoot.remove(lastSection)

            # COPY CHILDREN ELEMENTS OF BODY IN A LIST
            childrenList = root.findall('w:body/*', namespaces=NAMESPACES)

            # DELETE ALL CHILDREN OF BODY
            for child in root:
                if child.tag == '{%(w)s}body' % NAMESPACES:
                    child.clear()

            # REFILL BODY AND MERGE DOCS - ADD LAST SECTION ENCAPSULATED OR NOT
            lr = len(replacements)
            lc = len(childrenList)
            parts = []
            for i, repl in enumerate(replacements):
                for (j, n) in enumerate(childrenList):
                    element = deepcopy(n)
                    for child in root:
                        if child.tag == '{%(w)s}body' % NAMESPACES:
                            child.append(element)
                            parts.append(element)
                            if (j + 1) == lc:
                                if (i + 1) == lr:
                                    child.append(mainSection)
                                    parts.append(mainSection)
                                else:
                                    if sepClass == 'section':
                                        intSection = deepcopy(mainSection)
                                        p = etree.SubElement(child, '{%(w)s}p' % NAMESPACES)
                                        pPr = etree.SubElement(p, '{%(w)s}pPr' % NAMESPACES)
                                        pPr.append(intSection)
                                        parts.append(p)
                                    elif sepClass == 'break':
                                        pb = etree.SubElement(child, '{%(w)s}p' % NAMESPACES)
                                        r = etree.SubElement(pb, '{%(w)s}r' % NAMESPACES)
                                        nbreak = Element('{%(w)s}br' % NAMESPACES)
                                        nbreak.attrib['{%(w)s}type' % NAMESPACES] = type
                                        r.append(nbreak)

                    self.merge(parts, **repl)

    def merge_pages(self, replacements):
        """
        Deprecated method.
        """
        warnings.warn("merge_pages has been deprecated in favour of merge_templates",
                      category=DeprecationWarning,
                      stacklevel=2)
        self.merge_templates(replacements, "page_break")

    def merge(self, parts=None, **replacements):
        if not parts:
            parts = self.parts.values()

        for field, replacement in replacements.items():
            for part in parts:
                # to support sub rows merge
                if isinstance(replacement, list):
                    self.merge_rows(field, replacement,part)
                else:
                    self.__merge_field(part, field, replacement)

    def __merge_field(self, part, field, text):
        if field.endswith('_source'):
            if os.path.exists(text):
                # 此处检查确认是图片。如果是，读取到text变量。如果不是，删除原有的placeholder图片(save的时候查找删除)
                mimetype = mimetypes.guess_type(text)[0]
                if mimetype in ['image/bmp', 'image/jpeg', 'image/png', 'image/gif', 'image/x-icon']:
                    
                    # png出现问题，word会提示无法读取的内容，jpg正常。因此，转换
                    # print(text)
                    fileList = text.split('.')
                    extension = fileList[-1]
                    JPG_extension = "jpg"
                    JPG_FORMAT_file = "".join(fileList[:-1]) + "." + JPG_extension
                    

                    # 看是否需要转换
                    if not os.path.exists(JPG_FORMAT_file):
                        # print(JPG_FORMAT_file)
                        im = Image.open(text)

                        if im.mode in ("RGBA", "P"):
                            x,y = im.size 
                            try: 
                              # 使用白色来填充背景 from：www.jb51.net
                              # (alpha band as paste mask). 
                              p = Image.new('RGBA', im.size, (255,255,255))
                              p.paste(im, (0, 0, x, y), im)
                              im = p.convert("RGB")
                            except:
                              pass
                        im.save(JPG_FORMAT_file)


                    # 这个时候，text为文件绝对地址
                    img_name = field
                    # inline_img_el = part.find(
                    #      './/wp:docPr[@title="{}"]/..'.format("IMAGE:" + img_name), namespaces=NAMESPACES)
                    imglist = part.findall('.//wp:docPr[@title="{}"]/..'.format("IMAGE:" + img_name), namespaces=NAMESPACES)
                    if len(imglist) > 0:
                        for inline_img_el in imglist:
                            if inline_img_el is not None:
                                # print(inline_img_el)
                                embed_node = inline_img_el.find('.//a:blip', namespaces=NAMESPACES)

                                if embed_node is not None:
                                        # generate a random id and add tp media list for later export to media folder in zip file
                                    img_id = 'MMR{}'.format(randint(10000000, 999999999))
                                    with open(JPG_FORMAT_file, 'rb') as f:
                                        content = f.read()
                                    
                                    self.media[img_id + ':' + JPG_extension] = content
                                        # self.media[extension] = extension

                                        # add a relationship
                                    last_img_relationship = self.rels.findall(
                                            '{%(ns)s}Relationship[@Type="%(od)s/image"]' % self.RELS_NAMESPACES)[-1]
                                    new_img_relationship = deepcopy(last_img_relationship)
                                    new_img_relationship.set('Id', img_id)
                                    new_img_relationship.set('Target', 'media/{}.{}'.format(img_id, JPG_extension))
                                    self.rels.getroot().append(new_img_relationship)

                                        # replace the embed attrib with the new image_id
                                    embed_node = inline_img_el.find('.//a:blip', namespaces=NAMESPACES)
                                    embed_attr = embed_node.attrib.keys()[0]
                                    embed_node.attrib[embed_attr] = img_id
                                    # mark as done
                                inline_img_el.find(
                                        'wp:docPr', namespaces=NAMESPACES).attrib['title'] = 'replaced_image_{}'.format(img_id)
                                inline_img_el.find('wp:docPr', namespaces=NAMESPACES).attrib['descr'] = ''
                                # newId = str(randint(10000000000,99999999999))
                                # inline_img_el.find('wp:docPr', namespaces=NAMESPACES).attrib['id'] = newId
                                # inline_img_el.find('.//pic:cNvPr', namespaces=NAMESPACES).attrib['id'] = newId
            return

        for mf in part.findall('.//MergeField[@name="%s"]' % field):
            children = list(mf)
            mf.clear()  # clear away the attributes
            mf.tag = '{%(w)s}r' % NAMESPACES
            mf.extend(children)

            nodes = []
            # preserve new lines in replacement text
            if text!=0:
                text = text or ''  # text might be None
            text_parts = str(text).replace('\r', '').split('\n')
            for i, text_part in enumerate(text_parts):
                text_node = Element('{%(w)s}t' % NAMESPACES)
                text_node.text = text_part
                nodes.append(text_node)

                # if not last node add new line node
                if i < (len(text_parts) - 1):
                    nodes.append(Element('{%(w)s}br' % NAMESPACES))

            ph = mf.find('MergeText')
            if ph is not None:
                # add text nodes at the exact position where
                # MergeText was found
                index = mf.index(ph)
                for node in reversed(nodes):
                    mf.insert(index, node)
                mf.remove(ph)
            else:
                mf.extend(nodes)

    def merge_rows(self, anchor, rows, part=None):
        if part is not None:
            parts=[part]
        else:
            parts=None

        # notOnlyLeafTable = False
        # for index,item in enumerate(rows):
        #     if isinstance(item,dict):
        #         for k,v in item.items():
        #             if isinstance(v,list):
        #                 notOnlyLeafTable = True
        #                 break

        lists = self.__find_row_anchor(anchor,parts)
        for eachTable in lists:
            table, idx, template = eachTable
            if table is not None:
                if len(rows) > 0:
                    del table[idx]
                    for i, row_data in enumerate(rows):

                        row = deepcopy(template)
                        self.merge([row], **row_data)
                        table.insert(idx + i, row)
                else:
                    # if there is no data for a given table
                    # we check whether table needs to be removed
                    if self.remove_empty_tables:
                        parent = table.getparent()
                        parent.remove(table)

    def __find_row_anchor(self, field, parts=None):
        subTableFinding = False
        if not parts:
            parts = self.parts.values()
        else:
            subTableFinding = True
        # 目前，只支持二级数组的嵌套。
        for part in parts:
            dlist = []
            for table in part.findall('.//{%(w)s}tbl' % NAMESPACES):
                for idx, row in enumerate(table):
                    if row.find('.//MergeField[@name="%s"]' % field) is not None:
                        if subTableFinding:
                            if row.find('.//{%(w)s}tbl' % NAMESPACES) is None:
                                dlist.append((table, idx, row))
                        else:
                            # if notOnlyLeafTable:
                                # 取出临界table：再下一层就没有这个field的table
                            subTables = row.findall('.//{%(w)s}tbl' % NAMESPACES)
                            
                            for stable in subTables:
                                subTable = (table,idx,row)
                                for sidx,srow in enumerate(stable):
                                    # 如果还有field，就保留
                                    if srow.find('.//MergeField[@name="%s"]' % field) is not None:
                                        subTable = (stable,sidx,srow)
                            if subTable:
                                dlist.append(subTable)
                            # else:
                            #     if row.find('.//{%(w)s}tbl' % NAMESPACES) is None:
                            #         dlist.append((table, idx, row))
            if(len(dlist) > 0):
                # print(len(dlist))
                return dlist
        return []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        if self.zip is not None:
            try:
                self.zip.close()
            finally:
                self.zip = None