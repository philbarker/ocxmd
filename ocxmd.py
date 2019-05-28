from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import yaml, json, rdflib, ast

SCRIPT_STARTER = '<script type="application/ld+json">'


class OCXMetadata(Extension):
    """Python-Markdown extension for parsing OCX metadata from YAML."""

    def __init__(self, *args, **kwargs):
        # define config option for specifying JSON-LD context
        self.config = {
            "context": ["", "deprecated (JSON-LD context for YAML md)"],
            "YAMLcontext": ["", "YAML for JSON-LD context"],
            "TTLcontext": ["", "Turtle context header"],
        }
        super(OCXMetadata, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        md.registerExtension(self)
        self.md = md
        if self.getConfig("YAMLcontext"):
            # use YAMLcontext, even if both context and YAMLcontext are set
            self.md.YAMLcontext = self.getConfig("YAMLcontext")
        elif self.getConfig("context"):
            # context is deprecated but check for backward compatibility
            self.md.YAMLcontext = self.getConfig("context")
        else:
            self.md.YAMLcontext = ""
        if self.getConfig("TTLcontext"):
            # this is a string, easier for mkdocs yaml config?
            self.md.TTLcontext = ast.literal_eval(self.getConfig("TTLcontext"))
        else:
            self.md.TTLcontext = None
        md.preprocessors.register(OCXMetadataPreprocessor(md), "ocxmetadata", 28)


class OCXMetadataPreprocessor(Preprocessor):
    def process_yaml_block(self, lines, index):
        yaml_block = [self.md.YAMLcontext]  # start with the JSON-LD context
        g = rdflib.Graph()
        context = self.md.TTLcontext
        while lines:  # loop processing YAML block
            line = lines.pop(0)
            if line == "---":  # should be the end of a YAML block
                self.md.meta[index] = yaml.safe_load("\n".join(yaml_block))
                self.md.jsonld[index] = json.dumps(self.md.meta[index])
                new_line = SCRIPT_STARTER + self.md.jsonld[index] + "</script>"
                self.md.graphs[index] = g.parse(
                    data=self.md.jsonld[index], format="json-ld"
                )
                return new_line  # leave loop for processing YAML block
            else:  # if it's not the end of the YAML, add line to YAML
                yaml_block.append(line)

    def process_ttl_block(self, lines, index):
        ttl_block = []  # start with empty list context
        g = rdflib.Graph()
        context = self.md.TTLcontext
        while lines:  # loop processing TTL block
            line = lines.pop(0)
            if line == "---":  # should be the end of a YAML block
                turtle = "\n".join(ttl_block)
                self.md.graphs[index] = g.parse(data=turtle, format="turtle")
                self.md.jsonld[index] = g.serialize(
                    format="json-ld", indent=4, context=context
                ).decode("utf-8")
                self.md.meta[index] = ast.literal_eval(self.md.jsonld[index])
                new_line = SCRIPT_STARTER + self.md.jsonld[index] + "</script>"
                return new_line  # leave loop for processing YAML block
            else:  # if it's not the end of the YAML, add line to YAML
                ttl_block.append(line)

    def run(self, lines):
        new_lines = []
        count = 0  # running count of metadata blocks found
        self.md.meta = {}
        self.md.graphs = {}
        self.md.jsonld = {}
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
        if self.md.meta == {}:
            self.md.meta = None
        if self.md.graphs == {}:
            self.md.graphs = None
        if self.md.jsonld == {}:
            self.md.jsonld = None
        return new_lines


def makeExtension(**kwargs):
    # allows calling of extension by string which is not dot-noted
    return OCXMetadata(**kwargs)
