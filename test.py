import markdown, pytest
from ocxmd import OCXMetadata

TESTINPUT_1_1 = """---
"@context": "http://schema.org/"
"@id": "#lesson1"
"@type": "CreativeWork"
---
#YAML to JSON-LD test
I started with some YAML and turned it into JSON-LD
"""
TESTINPUT_1_2 = """---
"@id": "#lesson1"
"@type": "CreativeWork"
---
#YAML to JSON-LD test
I started with some YAML and turned it into JSON-LD
"""
TESTINPUT_1_1_TTL = """---TTL
@base <http://example.org> .
@prefix sdo: <http://schema.org/> .
@prefix ex: <http://example.org/> .
<#lecture1> a sdo:CreativeWork  .
---
#Turtle to JSON-LD test
I started with some Turtle and turned it into JSON-LD
"""

HTMLEXPECTED_1 = """<script type="application/ld+json">{"@context": "http://schema.org/", "@id": "#lesson1", "@type": "CreativeWork"}</script>

<h1>YAML to JSON-LD test</h1>
<p>I started with some YAML and turned it into JSON-LD</p>"""

METADATAEXPECTED_1 = {
    1: {"@context": "http://schema.org/", "@id": "#lesson1", "@type": "CreativeWork"}
}
METADATAEXPECTED_1_TTL = {
    1: '@base <http://example.org> .\n@prefix sdo: <http://schema.org/> .\n@prefix ex: <http://example.org/> .\n<#lecture1> a sdo:CreativeWork  .'
}
HTMLEXPECTED_1_TTL = """<script type="application/ld+json">[
    {
        "@id": "http://example.org#lecture1",
        "@type": [
            "http://schema.org/CreativeWork"
        ]
    }
]</script>

<h1>Turtle to JSON-LD test</h1>
<p>I started with some Turtle and turned it into JSON-LD</p>"""

TESTINPUT = """---
"@id": "#lesson1"
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
#YAML to JSON-LD test
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
"""
HTMLEXPECTED_3 = """<script type="application/ld+json">{"@context": ["http://schema.org", {"oer": "http://oerschema.org/"}, {"ocx": "https://github.com/K12OCX/k12ocx-specs/"}], "@id": "#lesson1", "name": "Test Lesson 1", "@type": ["oer:Lesson", "CreativeWork"], "learningResourceType": "LessonPlan", "hasPart": {"@id": "#activity1"}, "author": {"@type": "Person", "name": "Fred Blogs"}}</script>

<h1>YAML to JSON-LD test</h1>
<p>I started with some YAML and turned it into JSON-LD</p>
<p>Here is some more YAML</p>
<script type="application/ld+json">{"@context": ["http://schema.org", {"oer": "http://oerschema.org/"}, {"ocx": "https://github.com/K12OCX/k12ocx-specs/"}], "@id": "#activity1", "@type": ["oer:Activity", "CreativeWork"], "name": "Test Activity 1.1", "learningResourceType": "Activity"}</script>"""

HTMLEXPECTED_2 = """<script type="application/ld+json">{"@context": "http://schema.org", "@id": "#lesson1", "name": "Test Lesson 1", "@type": ["oer:Lesson", "CreativeWork"], "learningResourceType": "LessonPlan", "hasPart": {"@id": "#activity1"}, "author": {"@type": "Person", "name": "Fred Blogs"}}</script>

<h1>YAML to JSON-LD test</h1>
<p>I started with some YAML and turned it into JSON-LD</p>
<p>Here is some more YAML</p>
<script type="application/ld+json">{"@context": "http://schema.org", "@id": "#activity1", "@type": ["oer:Activity", "CreativeWork"], "name": "Test Activity 1.1", "learningResourceType": "Activity"}</script>"""


METADATAEXPECTED_2 = {
    1: {
        "@context": "http://schema.org",
        "@id": "#lesson1",
        "name": "Test Lesson 1",
        "@type": ["oer:Lesson", "CreativeWork"],
        "learningResourceType": "LessonPlan",
        "hasPart": {"@id": "#activity1"},
        "author": {"@type": "Person", "name": "Fred Blogs"},
    },
    2: {
        "@context": "http://schema.org",
        "@id": "#activity1",
        "@type": ["oer:Activity", "CreativeWork"],
        "name": "Test Activity 1.1",
        "learningResourceType": "Activity",
    },
}

METADATAEXPECTED_3 = {
    1: {
        "@context": [
            "http://schema.org",
            {"oer": "http://oerschema.org/"},
            {"ocx": "https://github.com/K12OCX/k12ocx-specs/"},
        ],
        "@id": "#lesson1",
        "name": "Test Lesson 1",
        "@type": ["oer:Lesson", "CreativeWork"],
        "learningResourceType": "LessonPlan",
        "hasPart": {"@id": "#activity1"},
        "author": {"@type": "Person", "name": "Fred Blogs"},
    },
    2: {
        "@context": [
            "http://schema.org",
            {"oer": "http://oerschema.org/"},
            {"ocx": "https://github.com/K12OCX/k12ocx-specs/"},
        ],
        "@id": "#activity1",
        "@type": ["oer:Activity", "CreativeWork"],
        "name": "Test Activity 1.1",
        "learningResourceType": "Activity",
    },
}


YAML_CONTEXT = """
"@context":
    - "http://schema.org"
    - "oer": "http://oerschema.org/"
    - "ocx": "https://github.com/K12OCX/k12ocx-specs/"
"""


def test1_1():
    md = markdown.Markdown(extensions=["ocxmd"])
    html = md.convert(TESTINPUT_1_1)
    assert md.meta == METADATAEXPECTED_1
    assert html == HTMLEXPECTED_1


def test1_2():
    md = markdown.Markdown(
        extensions=["ocxmd"],
        extension_configs={"ocxmd": {"context": "'@context' : 'http://schema.org'"}},
    )
    html = md.convert(TESTINPUT_1_1)
    assert md.meta == METADATAEXPECTED_1
    assert html == HTMLEXPECTED_1


def test2():
    md = markdown.Markdown(
        extensions=["ocxmd"],
        extension_configs={"ocxmd": {"context": "'@context' : 'http://schema.org'"}},
    )
    html = md.convert(TESTINPUT)
    assert md.meta == METADATAEXPECTED_2
    assert html == HTMLEXPECTED_2


def test3():
    md = markdown.Markdown(
        extensions=["ocxmd"], extension_configs={"ocxmd": {"context": YAML_CONTEXT}}
    )
    html = md.convert(TESTINPUT)
    assert md.meta == METADATAEXPECTED_3
    assert html == HTMLEXPECTED_3

def test1_1_TTL():
    md = markdown.Markdown(extensions=["ocxmd"])
    html = md.convert(TESTINPUT_1_1_TTL)
    print(md.meta)
    print(html)
    assert md.meta == METADATAEXPECTED_1_TTL
    assert html == HTMLEXPECTED_1_TTL
