from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.treeprocessors import Treeprocessor
import xml.etree.ElementTree as ET
import yaml, json, re

OCX_YAML_STARTER = '---'
YAML_CONTEXT = '''
"@context":
    - "http://schema.org"
    - "oer": "http://oerschema.org/"
    - "ocx": "https://github.com/K12OCX/k12ocx-specs/"
'''
SCRIPT_STARTER = '<script type="application/ld+json">'

class OCXMetadata(Extension):
    """Python-Markdown extension for parsing OCX metadata from YAML."""

    def extendMarkdown(self, md):
        md.registerExtension(self)
        self.md = md
        md.preprocessors.register(OCXMetadataPreprocessor(md), 'ocxmetadata', 28)
        md.treeprocessors.register(OCXTreeProcessor(md), 'ocxsection', 29)

class OCXTreeProcessor(Treeprocessor):
    START_SECTION_RE = re.compile('~~([SCHFNDA])([^~]*)~~')
    END_SECTION_RE = re.compile('~~/([SCHFNDA])~~')

    def run(self, root):
        ancestors = [root]
        self.section(root, ancestors)
        self.md.tree_diagram = ''
        self.set_tree_diagram(root, 0)

    def section(self, node, new_ancestors):
        # rebuild the elment tree by running through all the nodes, and recursively
        # through the children of those nodes, replacing any p elements that
        # indicate the start of a sectioning element (e.g. ~~S~~) with a new section
        # into which subsequent nodes are moved until an element indicating the
        # end of of a section.
        # node : element in oringinal eTree whose children are processed;
        # new_ancestors : stack of ancestors in eTree being created;
        # note, the node being processed won't be in the eTree created if it marks
        # the beginning of end of a section.
        # a list of nodes in the eTree at the start is made, new nodes are added
        # to the end of the eTree as they are processed, and the orginal node
        # removed.
        for child in list(node):
        # the list is immutable, so we run through the *original* nodes in the eTree
        # removing them when done and adding the new processed nodes to the end
            if child.text :
                start_match = self.START_SECTION_RE.match(child.text)
            else :
                start_match = False
            if start_match: # we have a node that indicates the start of a section
                # there is nothing to keep in such a node
                node.remove(child)
                # determine which sectioning elmt
                if 'S' == start_match.group(1).upper():
                    newsect_type = 'section'
                elif 'C' == start_match.group(1).upper():
                    newsect_type = 'chapter'
                elif 'A' == start_match.group(1).upper():
                    newsect_type = 'article'
                elif 'H' == start_match.group(1).upper():
                    newsect_type = 'header'
                elif 'F' == start_match.group(1).upper():
                    newsect_type = 'footer'
                elif 'N' == start_match.group(1).upper():
                    newsect_type = 'nav'
                elif 'D' == start_match.group(1).upper():
                    newsect_type = 'div'
                else :
                    newsect_type = 'div'
                # find id attribute of new section, if any
                attr = {"id": start_match.group(2).replace(' ','')} if start_match.group(2) else {}
                # create new section
                newsect = ET.SubElement(new_ancestors[-1], newsect_type, attr)
                # this new section will be the new parent until we get to end marker
                new_ancestors.append(newsect)
            elif (child.text and self.END_SECTION_RE.match(child.text.upper())):
                # we have reached an end of section marker
                # nothing to keep in such a node
                node.remove(child)
                # revert to using previous new_ancestor as new parent
                new_ancestors.pop()
            else :
                node.remove(child) # remove from original place in tree
                new_ancestors[-1].append(child) # append to the latest new ancestor
                self.section(child, new_ancestors) # recurse through nodes children

    def set_tree_diagram(self, node, depth):
        ldepth = depth + 1
        for child in list(node):
            attrib = str(child.attrib) if child.attrib else ''
            line = '\n'+ldepth*'    '+'|--'
            self.md.tree_diagram = self.md.tree_diagram+line+child.tag+attrib
            self.set_tree_diagram(child, ldepth)


class OCXMetadataPreprocessor(Preprocessor):
    def run(self, lines):
        new_lines = []
        yaml_store = {}
        yaml_count = 0
        while lines: #run through all the lines of md looking for YAML
            line = lines.pop(0)
            if line == '---': #should be start of a YAML block
                yaml_count += 1
                yaml_block = [YAML_CONTEXT]
                while lines: #loop processing YAML block
                    line = lines.pop(0)
                    if line == '---': #should be the end of a YAML block
                        yaml_store[yaml_count] = yaml.safe_load (
                            "\n".join(yaml_block)
                        )
                        new_line = SCRIPT_STARTER \
                           + json.dumps(yaml_store[yaml_count]) \
                           + '</script>'
                        new_lines.append(new_line)
                        break #leave loop for processing YAML block
                    else:
                        yaml_block.append(line)
            else:
                new_lines.append(line)
        if yaml_store:
            self.md.meta = yaml_store
        else:
            self.md.meta = None
        return new_lines

def makeExtension(**kwargs):
    # allows calling of extension by string which is not dot-noted
    return OCXMetadata(**kwargs)
