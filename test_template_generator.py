
import pytest
from template_generator import Introspected, Template, DataAssociation, create_associations

"""TODO:

    * Add properties?
"""

INTROSPECTION_1 = '''<?xml version='1.0' encoding='utf8'?>
<node name="/com/jogr/Test1">
    <interface name="com.jogr.Test1">
        <method name="TestMethod1">
            <arg direction="out" type="s" />
        </method>
    </interface>
</node>
'''

ASSOCIATIONS_1 = '''{
    "com.jogr.Test1": [
        {
            "name": "TestMethod1",
            "data": [
                [
                    [],
                    ["A string"]
                ]
            ]
        }
    ]
}
'''

# This is how the generated template based on INTROSPECTION_1 together with
# ASSOCIATIONS_1 should look
INTROSPECTION_1_GENERATED_TEMPLATE = '''
# This file has been generated to be used as a template with python-dbusmock.
# Do not edit this file manually, instead use introspection XML and data 
# associations json to generate it differently.

# These variables are required by python-dbusmock
BUS_NAME = "com.jogr.Test1"
MAIN_OBJ = "/com/jogr/Test1"
MAIN_IFACE = "com.jogr.Test1"
SYSTEM_BUS = False


def load(mock, parameters):
    """This method is required by python-dbusmock"""

    mock.AddMethods(MAIN_IFACE, [
        ("TestMethod1", "", "s", \'\'\'ret = eval("{(): \'A string\'}")[tuple(args)]\'\'\'),
    ])

'''

INTROSPECTION_2 = '''<?xml version='1.0' encoding='utf8'?>
<node name="/com/jogr/Test2">
    <interface name="com.jogr.Test2">
        <method name="TestMethod1">
            <arg direction="out" type="s" />
        </method>
        <method name="TestMethod2">
            <arg direction="in" type="s" />
        </method>
    </interface>
</node>
'''

ASSOCIATIONS_2 = '''{
    "com.jogr.Test2": [
        {
            "name": "TestMethod1",
            "data": [
                [
                    [],
                    ["A string"]
                ]
            ]
        },
        {
            "name": "TestMethod2",
            "data": [
                [
                    ["A string"],
                    []
                ]
            ]
        }
    ]
}
'''

# This is how the generated template based on INTROSPECTION_2 together with
# ASSOCIATIONS_2 should look
INTROSPECTION_2_GENERATED_TEMPLATE = '''
# This file has been generated to be used as a template with python-dbusmock.
# Do not edit this file manually, instead use introspection XML and data 
# associations json to generate it differently.

# These variables are required by python-dbusmock
BUS_NAME = "com.jogr.Test2"
MAIN_OBJ = "/com/jogr/Test2"
MAIN_IFACE = "com.jogr.Test2"
SYSTEM_BUS = False


def load(mock, parameters):
    """This method is required by python-dbusmock"""

    mock.AddMethods(MAIN_IFACE, [
        ("TestMethod2", "s", "", \'\'\'ret = None\'\'\'),
    ])
    mock.AddMethods(MAIN_IFACE, [
        ("TestMethod1", "", "s", \'\'\'ret = eval("{(): \'A string\'}")[tuple(args)]\'\'\'),
    ])

'''

INTROSPECTION_3 = '''<?xml version='1.0' encoding='utf8'?>
<node name="/com/jogr/Test3">
    <interface name="com.jogr.Test3">
        <method name="TestMethod1">
            <arg direction="out" type="i" />
            <arg direction="in" type="iii" />
        </method>
    </interface>
</node>
'''


class TestIntrospected(object):

    def test_interface_name_is_correct(self):
        i = Introspected(INTROSPECTION_1)
        assert i.interface_names()[0] == "com.jogr.Test1"

    def test_node_name_is_correct(self):
        i = Introspected(INTROSPECTION_1)
        assert i.node_name() == "/com/jogr/Test1"

    def test_method_by_name_returns_none_when_invalid(self):
        expected_name = "TestMethodXXX"
        i = Introspected(INTROSPECTION_2)
        method = i.method_by_name(expected_name)
        assert method == None

    @pytest.mark.parametrize(("name, in_args, out_args"), [
        ("TestMethod1", "", "i"),
        ("TestMethod2", "iii", "i"),
        ("TestMethod3", "ss", "i"),
        ("TestMethod4", "s", "i"),
        ("TestMethod5", "s", ""),
        ("TestMethod6", "", "ii"),
        ("TestMethod7", "s", "ss"),
    ])
    def test_returns_correct_methods(self, name, in_args, out_args):
        i = Introspected(INTROSPECTION_4)
        method = i.method_by_name(name)
        assert method.name() == name
        assert method.in_args() == in_args
        assert method.out_args() == out_args


class TestTemplate(object):

    @pytest.mark.parametrize(("introspection, association, template"), [
        (INTROSPECTION_1, ASSOCIATIONS_1, INTROSPECTION_1_GENERATED_TEMPLATE),
        (INTROSPECTION_2, ASSOCIATIONS_2, INTROSPECTION_2_GENERATED_TEMPLATE),
    ])
    def test_generated_template_code(self, introspection, association, template):
        i = Introspected(introspection)
        t = Template(i)
        associations = create_associations(association)
        t.apply_data_associations(associations)
        generated_template = t.create_template()
        assert generated_template == template


INTROSPECTION_4 = '''<?xml version='1.0' encoding='utf8'?>
<node name="/com/jogr/Test4">
    <interface name="com.jogr.Test4">
        <method name="TestMethod1">
            <arg direction="out" type="i" />
            <arg direction="in" type="" />
        </method>
        <method name="TestMethod2">
            <arg direction="out" type="i" />
            <arg direction="in" type="iii" />
        </method>
        <method name="TestMethod3">
            <arg direction="out" type="i" />
            <arg direction="in" type="ss" />
        </method>
        <method name="TestMethod4">
            <arg direction="out" type="i" />
            <arg direction="in" type="s" />
        </method>
        <method name="TestMethod5">
            <arg direction="out" type="" />
            <arg direction="in" type="s" />
        </method>
        <method name="TestMethod6">
            <arg direction="out" type="ii" />
            <arg direction="in" type="" />
        </method>
        <method name="TestMethod7">
            <arg direction="out" type="ss" />
            <arg direction="in" type="s" />
        </method>
        <method name="TestMethod8">
            <arg direction="out" type="i" />
            <arg direction="in" type="sss" />
        </method>
    </interface>
</node>
'''

association_1 = DataAssociation("TestMethod1", [((1, 2, 3), 101)])
expected_1 = '''ret = eval("{(1, 2, 3): 101}")[tuple(args)]'''

association_2 = DataAssociation("TestMethod2", [((), 101)])
expected_2 = '''ret = eval("{(): 101}")[tuple(args)]'''

association_3 = DataAssociation("TestMethod3", [(("One", "Two"), 101)])
expected_3 = '''ret = eval("{('One', 'Two'): 101}")[tuple(args)]'''

association_4 = DataAssociation("TestMethod4", [(("One"), "Return One")])
expected_4 = '''ret = eval("{'One': 'Return One'}")[args.pop()]'''

association_5 = DataAssociation("TestMethod5", [(("One"), [])])
expected_5 = '''ret = None'''

association_6 = DataAssociation("TestMethod6", [((), [1, 2])])
expected_6 = '''ret = eval("{(): [1, 2]}")[tuple(args)]'''

association_7 = DataAssociation("TestMethod7", [("A string", ["1", "2"])])
expected_7 = '''ret = eval("{'A string': ['1', '2']}")[args.pop()]'''

association_8 = DataAssociation("TestMethod8", [(("1", "2", "3"), (1)), (("one", "two", "three"), (2))])
expected_8 = '''ret = eval("{('1', '2', '3'): 1,('one', 'two', 'three'): 2}")[tuple(args)]'''

class TestMethod(object):

    @pytest.mark.parametrize(("method_name, association, expected"), [
        ("TestMethod1", association_1, expected_1),
        ("TestMethod2", association_2, expected_2),
        ("TestMethod3", association_3, expected_3),
        ("TestMethod4", association_4, expected_4),
        ("TestMethod5", association_5, expected_5),
        ("TestMethod6", association_6, expected_6),
        ("TestMethod7", association_7, expected_7),
        ("TestMethod8", association_8, expected_8),
    ])
    def test_associations(self, method_name, association, expected):
        i = Introspected(INTROSPECTION_4)
        method = i.method_by_name(method_name)
        method.apply_associations(association)
        # 'encode()' is to not compare with escaped quotes in the string
        assert method.stub().encode() == expected

