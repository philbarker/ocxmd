from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import yaml, json

OCX_YAML_STARTER = "---"
YAML_CONTEXT = """
"@context": "http://schema.org"
"""
SCRIPT_STARTER = '<script type="application/ld+json">'


class OCXMetadata(Extension):
    """Python-Markdown extension for parsing OCX metadata from YAML."""

    def __init__(self, *args, **kwargs):
        # define config option for specifying JSON-LD context
        self.config = {"context": [YAML_CONTEXT, "Specify JSON-LD context"]}
        super(OCXMetadata, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        md.registerExtension(self)
        self.md = md
        self.md.context = self.getConfig("context")
        md.preprocessors.register(OCXMetadataPreprocessor(md), "ocxmetadata", 28)


class OCXMetadataPreprocessor(Preprocessor):
    def run(self, lines):
        new_lines = []
        yaml_store = {}
        yaml_count = 0
        yaml_context = self.md.context
        while lines:  # run through all the lines of md looking for YAML
            line = lines.pop(0)
            if line == "---":  # should be start of a YAML block
                yaml_count += 1
                yaml_block = [yaml_context]
                while lines:  # loop processing YAML block
                    line = lines.pop(0)
                    if line == "---":  # should be the end of a YAML block
                        yaml_store[yaml_count] = yaml.safe_load("\n".join(yaml_block))
                        new_line = (
                            SCRIPT_STARTER
                            + json.dumps(yaml_store[yaml_count])
                            + "</script>"
                        )
                        new_lines.append(new_line)
                        break  # leave loop for processing YAML block
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
