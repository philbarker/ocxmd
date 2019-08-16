import markdown, pytest
from rdflib import Graph, compare
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
@base <http://schema.org/> .
@prefix ex: <http://example.org#> .
ex:lecture1 a <CreativeWork> .
---
#Turtle to JSON-LD test
I started with some Turtle and turned it into JSON-LD
"""

TTL_1_1 = """@base <http://schema.org/> .
@prefix ex: <http://example.org#> .
ex:lecture1 a <CreativeWork> .
"""

METADATAEXPECTED_1_1_TTL = {
    1: {
        "@context": {
            "@vocab": "http://schema.org/",
            "ocx": "https://github.com/K12OCX/k12ocx-specs/",
            "oer": "http://oerschema.org",
        },
        "@id": "http://example.org#lecture1",
        "@type": "CreativeWork",
    }
}

HTMLEXPECTED_1 = """<script type="application/ld+json">{"@context": "http://schema.org/", "@id": "#lesson1", "@type": "CreativeWork"}</script>

<h1>YAML to JSON-LD test</h1>
<p>I started with some YAML and turned it into JSON-LD</p>"""

JSONEXPECTED_1 = (
    """{"@context": "http://schema.org/", "@id": "#lesson1", "@type": "CreativeWork"}"""
)

METADATAEXPECTED_1 = {
    1: {"@context": "http://schema.org/", "@id": "#lesson1", "@type": "CreativeWork"}
}
METADATAEXPECTED_1_TTL = {
    1: "@base <http://schema.org/> .\n@prefix ex: <http://example.org#> .\nex:lecture1 a <CreativeWork> ."
}
HTMLEXPECTED_1_TTL = """<script type="application/ld+json">{
    "@context": {
        "@vocab": "http://schema.org/",
        "ocx": "https://github.com/K12OCX/k12ocx-specs/",
        "oer": "http://oerschema.org"
    },
    "@id": "http://example.org#lecture1",
    "@type": "CreativeWork"
}</script>

<h1>Turtle to JSON-LD test</h1>
<p>I started with some Turtle and turned it into JSON-LD</p>"""
JSONEXPECTED_1_TTL = {
    1: """{
    "@context": {
        "@vocab": "http://schema.org/",
        "ocx": "https://github.com/K12OCX/k12ocx-specs/",
        "oer": "http://oerschema.org"
    },
    "@id": "http://example.org#lecture1",
    "@type": "CreativeWork"
}"""
}
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

JSONEXPECTED_3 = {
    1: '{"@context": ["http://schema.org", {"oer": "http://oerschema.org/"}, {"ocx": "https://github.com/K12OCX/k12ocx-specs/"}], "@id": "#lesson1", "name": "Test Lesson 1", "@type": ["oer:Lesson", "CreativeWork"], "learningResourceType": "LessonPlan", "hasPart": {"@id": "#activity1"}, "author": {"@type": "Person", "name": "Fred Blogs"}}',
    2: '{"@context": ["http://schema.org", {"oer": "http://oerschema.org/"}, {"ocx": "https://github.com/K12OCX/k12ocx-specs/"}], "@id": "#activity1", "@type": ["oer:Activity", "CreativeWork"], "name": "Test Activity 1.1", "learningResourceType": "Activity"}',
}

HTMLEXPECTED_2 = """<script type="application/ld+json">{"@context": "http://schema.org", "@id": "#lesson1", "name": "Test Lesson 1", "@type": ["oer:Lesson", "CreativeWork"], "learningResourceType": "LessonPlan", "hasPart": {"@id": "#activity1"}, "author": {"@type": "Person", "name": "Fred Blogs"}}</script>

<h1>YAML to JSON-LD test</h1>
<p>I started with some YAML and turned it into JSON-LD</p>
<p>Here is some more YAML</p>
<script type="application/ld+json">{"@context": "http://schema.org", "@id": "#activity1", "@type": ["oer:Activity", "CreativeWork"], "name": "Test Activity 1.1", "learningResourceType": "Activity"}</script>"""

JSONEXPECTED_2 = {
    1: '{"@context": "http://schema.org", "@id": "#lesson1", "name": "Test Lesson 1", "@type": ["oer:Lesson", "CreativeWork"], "learningResourceType": "LessonPlan", "hasPart": {"@id": "#activity1"}, "author": {"@type": "Person", "name": "Fred Blogs"}}',
    2: '{"@context": "http://schema.org", "@id": "#activity1", "@type": ["oer:Activity", "CreativeWork"], "name": "Test Activity 1.1", "learningResourceType": "Activity"}',
}

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

TESTINPUT_MIXED = """---TTL
@base <http://example.org> .
@prefix : <http://schema.org/> .
@prefix oer: <http://oerschema.org/> .
<#lecture1>
    a :CreativeWork ;
    :name "Test Lesson 1" ;
    :learningResourceType "LessonPlan" ;
    :hasPart <#activity1> ;
    :author [
        a :Person ;
        :name "Fred Blogs"
    ] .
---
#Turtle and YAML to JSON-LD test
I started with some Turtle and turned it into JSON-LD

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

TTL_MIXED = """@base <http://example.org> .
@prefix : <http://schema.org/> .
@prefix oer: <http://oerschema.org/> .
<#lecture1>
    a :CreativeWork ;
    :name "Test Lesson 1" ;
    :learningResourceType "LessonPlan" ;
    :hasPart <#activity1> ;
    :author [
        a :Person ;
        :name "Fred Blogs"
    ] .
"""

METADATAEXPECTED_MIXED = {
    1: {
        "@context": {
            "@vocab": "http://schema.org/",
            "ocx": "https://github.com/K12OCX/k12ocx-specs/",
            "oer": "http://oerschema.org",
        },
        "@graph": [
            {
                "@id": "http://example.org#lecture1",
                "@type": "CreativeWork",
                "author": {"@id": "_:ub5bL8C13"},
                "hasPart": {"@id": "http://example.org#activity1"},
                "learningResourceType": "LessonPlan",
                "name": "Test Lesson 1",
            },
            {"@id": "_:ub5bL8C13", "@type": "Person", "name": "Fred Blogs"},
        ],
    },
    2: {
        "@id": "#activity1",
        "@type": ["oer:Activity", "CreativeWork"],
        "name": "Test Activity 1.1",
        "learningResourceType": "Activity",
    },
}

JSONEXPECTED_MIXED = {
    1: """{
    "@context": {
        "@vocab": "http://schema.org/",
        "ocx": "https://github.com/K12OCX/k12ocx-specs/",
        "oer": "http://oerschema.org"
    },
    "@graph": [
        {
            "@id": "http://example.org#lecture1",
            "@type": "CreativeWork",
            "author": {
                "@id": "_:ub5bL8C13"
            },
            "hasPart": {
                "@id": "http://example.org#activity1"
            },
            "learningResourceType": "LessonPlan",
            "name": "Test Lesson 1"
        },
        {
            "@id": "_:ub5bL8C13",
            "@type": "Person",
            "name": "Fred Blogs"
        }
    ]
}""",
    2: '{"@id": "#activity1", "@type": ["oer:Activity", "CreativeWork"], "name": "Test Activity 1.1", "learningResourceType": "Activity"}',
}

HTMLEXPECTED_MIXED = """<script type="application/ld+json">{
    "@context": {
        "@vocab": "http://schema.org/",
        "ocx": "https://github.com/K12OCX/k12ocx-specs/",
        "oer": "http://oerschema.org"
    },
    "@graph": [
        {
            "@id": "http://example.org#lecture1",
            "@type": "CreativeWork",
            "author": {
                "@id": "_:ub5bL8C13"
            },
            "hasPart": {
                "@id": "http://example.org#activity1"
            },
            "learningResourceType": "LessonPlan",
            "name": "Test Lesson 1"
        },
        {
            "@id": "_:ub5bL8C13",
            "@type": "Person",
            "name": "Fred Blogs"
        }
    ]
}</script>

<h1>Turtle and YAML to JSON-LD test</h1>
<p>I started with some Turtle and turned it into JSON-LD</p>
<p>Here is some more YAML</p>
<script type="application/ld+json">{"@id": "#activity1", "@type": ["oer:Activity", "CreativeWork"], "name": "Test Activity 1.1", "learningResourceType": "Activity"}</script>"""

YAML_CONTEXT = """
"@context":
    - "http://schema.org"
    - "oer": "http://oerschema.org/"
    - "ocx": "https://github.com/K12OCX/k12ocx-specs/"
"""

TTL_CONTEXT = """{
    "@vocab": "http://schema.org/",
    "oer": "http://oerschema.org",
    "ocx": "https://github.com/K12OCX/k12ocx-specs/",
}"""


def test1_1():
    md = markdown.Markdown(extensions=["ocxmd"])
    html = md.convert(TESTINPUT_1_1)
    assert md.meta == METADATAEXPECTED_1
    assert len(md.graphs) == 1
    assert md.jsonld[1] == JSONEXPECTED_1
    assert html == HTMLEXPECTED_1


def test1_2():
    # use context keyword keep as test for backward compatibility
    md = markdown.Markdown(
        extensions=["ocxmd"],
        extension_configs={
            "ocxmd": {"YAMLcontext": "'@context' : 'http://schema.org'"}
        },
    )
    html = md.convert(TESTINPUT_1_1)
    assert md.meta == METADATAEXPECTED_1
    assert len(md.graphs) == 1
    assert md.jsonld[1] == JSONEXPECTED_1
    assert html == HTMLEXPECTED_1


def test1_2_deprecated():
    # use context keyword keep as test for backward compatibility
    md = markdown.Markdown(
        extensions=["ocxmd"],
        extension_configs={"ocxmd": {"context": "'@context' : 'http://schema.org'"}},
    )
    html = md.convert(TESTINPUT_1_1)
    assert md.meta == METADATAEXPECTED_1


def test2():
    md = markdown.Markdown(
        extensions=["ocxmd"],
        extension_configs={
            "ocxmd": {"YAMLcontext": "'@context' : 'http://schema.org'"}
        },
    )
    html = md.convert(TESTINPUT)
    assert md.meta == METADATAEXPECTED_2
    g = Graph().parse(data='', format="turtle")
    assert compare.similar(md.graphs[1], g)
    assert md.jsonld == JSONEXPECTED_2
    assert html == HTMLEXPECTED_2


def test3():
    md = markdown.Markdown(
        extensions=["ocxmd"], extension_configs={"ocxmd": {"YAMLcontext": YAML_CONTEXT}}
    )
    html = md.convert(TESTINPUT)
    g = Graph().parse(data='', format="turtle")
    assert md.meta == METADATAEXPECTED_3
#to do: write sensible test for graph (need to check parsing is as expected, so look at triples)
    assert compare.similar(md.graphs[1], g)
    assert md.jsonld == JSONEXPECTED_3
    assert html == HTMLEXPECTED_3


def test1_1_TTL():
    md = markdown.Markdown(
        extensions=["ocxmd"], extension_configs={"ocxmd": {"TTLcontext": TTL_CONTEXT}}
    )
    html = md.convert(TESTINPUT_1_1_TTL)
    g = Graph().parse(data=TTL_1_1, format="turtle")
    assert md.meta == METADATAEXPECTED_1_1_TTL
    assert compare.similar(md.graphs[1], g)
    assert md.jsonld == JSONEXPECTED_1_TTL
    assert html == HTMLEXPECTED_1_TTL


def test_Mixed():
    md = markdown.Markdown(
        extensions=["ocxmd"], extension_configs={"ocxmd": {"TTLcontext": '{"@vocab": "http://schema.org/","oer": "http://oerschema.org","ocx": "https://github.com/K12OCX/k12ocx-specs/"}'}}
    )
    html = md.convert(TESTINPUT_MIXED)
    g_ttl = Graph().parse(data=TTL_MIXED, format="turtle")
    assert md.meta == METADATAEXPECTED_MIXED
    assert compare.similar(md.graphs[1], g_ttl)
    assert html == HTMLEXPECTED_MIXED
    assert md.jsonld == JSONEXPECTED_MIXED
