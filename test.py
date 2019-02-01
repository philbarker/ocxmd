import markdown, unittest
from ocxmd import OCXMetadata
TESTINPUT = '''
~~C lesson1~~

---
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

~~H~~
#YAML to JSON-LD test
I started with some YAML and turned it into JSON-LD

~~/H~~

~~S activity1~~

Here is some more YAML

---
"@id": "#activity1"
"@type":
    - oer:Activity
    - CreativeWork
name: "Test Activity 1.1"
learningResourceType: Activity
---
~~/S~~

~~/C~~
'''
HTMLEXPECTED = '''<chapter id="lesson1"><script type="application/ld+json">{"@context": ["http://schema.org", {"oer": "http://oerschema.org/"}, {"ocx": "https://github.com/K12OCX/k12ocx-specs/"}], "@id": "#lesson1", "name": "Test Lesson 1", "@type": ["oer:Lesson", "CreativeWork"], "learningResourceType": "LessonPlan", "hasPart": {"@id": "#activity1"}, "author": {"@type": "Person", "name": "Fred Blogs"}}</script>
<header><h1>YAML to JSON-LD test</h1><p>I started with some YAML and turned it into JSON-LD</p></header><section id="activity1"><p>Here is some more YAML</p><script type="application/ld+json">{"@context": ["http://schema.org", {"oer": "http://oerschema.org/"}, {"ocx": "https://github.com/K12OCX/k12ocx-specs/"}], "@id": "#activity1", "@type": ["oer:Activity", "CreativeWork"], "name": "Test Activity 1.1", "learningResourceType": "Activity"}</script>
</section></chapter>'''
METADATAEXPECTED = {1: {'@context': ['http://schema.org', {'oer': 'http://oerschema.org/'}, {'ocx': 'https://github.com/K12OCX/k12ocx-specs/'}], '@id': '#lesson1', 'name': 'Test Lesson 1', '@type': ['oer:Lesson', 'CreativeWork'], 'learningResourceType': 'LessonPlan', 'hasPart': {'@id': '#activity1'}, 'author': {'@type': 'Person', 'name': 'Fred Blogs'}}, 2: {'@context': ['http://schema.org', {'oer': 'http://oerschema.org/'}, {'ocx': 'https://github.com/K12OCX/k12ocx-specs/'}], '@id': '#activity1', '@type': ['oer:Activity', 'CreativeWork'], 'name': 'Test Activity 1.1', 'learningResourceType': 'Activity'}}
STRUCTUREEXPECTED = '''\n    |--chapter{'id': 'lesson1'}\n        |--p\n        |--header\n            |--h1\n            |--p\n        |--section{'id': 'activity1'}\n            |--p\n            |--p'''
class TestOCXMD(unittest.TestCase):
    md = markdown.Markdown(extensions = ['ocxmd'])
    html = md.convert(TESTINPUT)
    print(md.tree_diagram)
    print(md.meta)
    print(html)
    def test_html(self):
        self.assertEqual(self.html, HTMLEXPECTED)
    def test_md(self):
        self.assertEqual(self.md.meta, METADATAEXPECTED)
    def test_struct(self):
        self.assertEqual(self.md.tree_diagram, STRUCTUREEXPECTED)

if '__main__' == __name__:
    unittest.main()
