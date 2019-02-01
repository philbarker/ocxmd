An extension to [python markdown](https://python-markdown.github.io/) that:
- allows you to add semantic HTML5 sectioning elements into the generated html by putting strings such as `~~S~~` at the start of a section and `~~/S~~` at the end. Sectioning elements supported are `section` (S), `chapter` (C) `header` (H) `footer` (F) `nav` (N) `div` (D) and `article` (A). These can be given identifiers by add text after the sectioning element letter, e.g. `~~S lesson1~~`. Spaces in the identifier are removed. So `~~A activity 1~~` becomes `<article id="activity1">`.
- takes metadata embedded as YAML in a page of markdown and render it as JSON-LD in the HTML created by [MkDocs](https://www.mkdocs.org/). The extracted metadata is also returned as a python dict in the markdown object.

Currently it is focussed on schema.org and other metadata schema used by the [K12-OCX project](https://github.com/K12OCX/k12ocx-specs) for curriculum content materials (learning resources).

## Test metadata
YAML input
```
"@id": "#lesson1"
"@type":
    - oer:Lesson
    - CreativeWork
learningResourceType: LessonPlan
hasPart: {
  "@id": "#activity1"
}
author:
    "@type": Person
    name: Fred Blogs

```

JSON-LD output
```
<script type="application/ld+json">
{ "@context": [ "http://schema.org",
    { "oer": "http://oerschema.org/",
      "ocx": "https://github.com/K12OCX/k12ocx-specs/",
    }
  ],
  "@id": "#lesson1",
  "@type":["CreativeWork", "oer:Lesson"],
  "learningResourceType": "LessonPlan",
  "name": "Practice Counting Strategies",
  "hasPart": {
    "@id": "#activity1-1"
  }
  "author": {
    "@type": "Person"
    "name": "Fred"
  }
}
</script>
```

See test.py for a fully working example embedded in markdown.

## Requirements & dependencies
Python 3 (tested on Python 3.6.7)

Designed for use with [MkDocs](https://www.mkdocs.org/#installation)

Uses python packages [Python-Markdown](https://python-markdown.github.io/install/), [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation) and [json](https://docs.python.org/3.7/library/json.html).

Installation with setup.py requires [setuptools](https://setuptools.readthedocs.io/en/latest/setuptools.html#installing-setuptools)

Doesn't play nicely with other python markdown extensions that use `---` to delineate YAML (or anything else), notably the meta extension.

## Installation
(Warning: exercise caution thi searly release software with no warranty, test this first in a virtual environment!)
```
(venv)$ git clone https://github.com/philbarker/ocxmd.git
(venv)$ cd ocxmd
(venv)$ python setup.py test
(venv)$ python setup.py install
(venv)$ python test.py
```


## Usage
Add `ocxmd` to your extensions block in mkdocs.yml:
```
markdown_extensions:
  - ocxmd
```

The YAML must be separated from the rest of the markdown text by `---` before and after.

```
#YAML to JSON-LD test
---
"@id": "#Lesson1"
name: "Test Lesson 1"
"@type":
    - oer:Lesson
    - CreativeWork
learningResourceType: LessonPlan
hasPart: {
  "@id": "#activity1"
}
author:
    "@type": Person
    name: Fred Blogs
---

I started with some YAML and turned it into JSON-LD

Here is some more YAML
---
"@id": "#activity1"
"@type":
    - oer:Activity
    - CreativeWork
name: "Test Activity 1.1"
learningResourceType: Activity
---

```
All going well you will have to view source or inspect the HTML to see the output.

Can also be used in python to get metadata from YAML as a python dict

``` python
import markdown
from ocxmd import OCXMetadata
TESTINPUT = '''
#YAML to JSON-LD test
---
"@id": "#Lesson1"
name: "Test Lesson 1"
---
I started with some YAML and turned it into JSON-LD
'''
md = markdown.Markdown(extensions = ['ocxmd'])
print( md.convert(TESTINPUT) )
print( md.meta )
```

## Acknowledgements
I was helped in writing this by reference to Nikita Sivakov's [full-yaml-metadata extension](https://github.com/sivakov512/python-markdown-full-yaml-metadata)
