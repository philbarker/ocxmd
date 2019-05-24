from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import yaml, json, rdflib

SCRIPT_STARTER = '<script type="application/ld+json">'


class OCXMetadata(Extension):
    """Python-Markdown extension for parsing OCX metadata from YAML."""

    def __init__(self, *args, **kwargs):
        # define config option for specifying JSON-LD context
        self.config = {"context": ["", "Specify JSON-LD context"]}
        super(OCXMetadata, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        md.registerExtension(self)
        self.md = md
        self.md.context = self.getConfig("context")
        md.preprocessors.register(OCXMetadataPreprocessor(md), "ocxmetadata", 28)


class OCXMetadataPreprocessor(Preprocessor):
    def process_yaml_block(self, lines, index):
        yaml_block = [self.md.context]  # start with the JSON-LD context
        while lines:  # loop processing YAML block
            line = lines.pop(0)
            if line == "---":  # should be the end of a YAML block
                self.yaml[index] = yaml.safe_load("\n".join(yaml_block))
                new_line = SCRIPT_STARTER + json.dumps(self.yaml[index]) + "</script>"
                return new_line  # leave loop for processing YAML block
            else:  # if it's not the end of the YAML, add line to YAML
                yaml_block.append(line)

    def process_ttl_block(self, lines, index):
        ttl_block = []  # start with empty list context
        g = rdflib.Graph()
        context = {
            "@vocab": "http://schema.org/",
            "oer": "http://oerschema.org",
            "ocx": "https://github.com/K12OCX/k12ocx-specs/",
        }
        while lines:  # loop processing TTL block
            line = lines.pop(0)
            if line == "---":  # should be the end of a YAML block
                turtle = "\n".join(ttl_block)
                self.md.graphs[index] = g.parse(data=turtle, format="turtle")
                json_md = g.serialize(
                    format="json-ld", indent=4, context=context
                ).decode("utf-8")
                new_line = SCRIPT_STARTER + json_md + "</script>"
                return new_line  # leave loop for processing YAML block
            else:  # if it's not the end of the YAML, add line to YAML
                ttl_block.append(line)

    def run(self, lines):
        new_lines = []
        count = 0  # running count of metadata blocks found
        self.yaml = {}
        self.md.graphs = {}
        # run through all the lines of md looking for metadata blocks
        while lines:
            line = lines.pop(0)
            if line == "---":  # should be start of a YAML block
                count += 1
                new_lines.append(self.process_yaml_block(lines, count))
            elif line == "---TTL":  # should be start of a TTL block
                count += 1
                new_lines.append(self.process_ttl_block(lines, count))
            else:
                new_lines.append(line)
        if self.yaml:
            self.md.meta = self.yaml
        else:
            self.md.meta = None
        return new_lines


def makeExtension(**kwargs):
    # allows calling of extension by string which is not dot-noted
    return OCXMetadata(**kwargs)
