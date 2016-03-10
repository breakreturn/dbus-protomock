
D-Bus Protomock
==============

This project can generate templates for use with python-dbusmock.

By running `template_generator` and providing it with a D-Bus introspection XML file,
a data associations file, and an output location, there will be templates generated
which can be used with python-dbusmock. The templates will have the interface defined
in the D-Bus introspection XML and the methods will return values based on what input
is sent when calling them. This input is matched to the output in the data
associations file.

Dependencies
------------
This project depends on:

 * python-dbusmock
 * py.test (for running unit tests)

Usage
-----
To create a template `x.py` (in output directory `generated`) from inrospection
XML `x.xml` and associating input data with output values in data
associations file `x.json`, run:

    python template_generator x.xml x.json generated/

The generated template can be used with `python-dbusmock` like so:

    python -m dbusmock -t generated/x.py

Data format
-----------
A data associations file has the following json format:

    {
        "com.jogr.X": [
            {
                "name": "Ping",
                "data": [
                    [
                        ["Hello world"],
                        ["Hello back"]
                    ],
                    [
                        ["Good bye"],
                        ["Bye"]
                    ]
                ]
            }
        ]
    }

The 'com.jogr.X' object should correspond to the 'interface name' of the D-Bus
introspection XML. Its value is an array of objects that each have a 'name' which
correspond to 'method name' in the D-Bus introspection XML, and 'data' which associates
input values with output values. In the example above the input string "Hello world"
is associated with the output string "Hello back".

In practice this means that if
`Ping` is called like so:

    Ping("Hello world")

the reply would be:

    "Hello back"

The corresponding D-Bus XML could look like so:

    <?xml version='1.0' encoding='utf8'?>
    <node name="/com/jogr/X">
        <interface name="com.jogr.X">
            <method name="Ping">
                <arg direction="in" type="s" />
                <arg direction="out" type="s" />
            </method>
        </interface>
    </node>



Testing
-------
Run `py.test` in the project root.
