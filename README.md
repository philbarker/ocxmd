An extension to [python markdown](https://python-markdown.github.io/) that takes metadata embedded as YAML in a page of markdown and render it as JSON-LD in the HTML created by [MkDocs](https://www.mkdocs.org/). The extracted metadata is also returned as a python dict in the markdown object.

Currently it is focussed on schema.org and other metadata schema used by the [K12-OCX project](https://github.com/K12OCX/k12ocx-specs) for curriculum content materials (learning resources).

## Test metadata
YAML input
```
"@id": "#Lesson1"
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
  "@id": "#Lesson1",
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

## Usage
The YAML must be separated from the rest of the text by `---` before and after.


## Acknowledgements
I was helped in writing this by reference to Nikita Sivakov's [full-yaml-metadata extension](https://github.com/sivakov512/python-markdown-full-yaml-metadata)
