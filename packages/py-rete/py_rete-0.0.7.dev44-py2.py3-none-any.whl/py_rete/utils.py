import xml.etree.ElementTree as ET
from py_rete.conditions import AND
from py_rete.conditions import Cond
from py_rete.conditions import Neg
from py_rete.conditions import Filter
from py_rete.conditions import Bind
from py_rete.conditions import Ncc
from py_rete.common import V


def parse_json(s):
    """
    Parse a JSON representation of knowledge.
    """
    raise NotImplementedError


def parse_xml(s):
    root = ET.fromstring(s)
    result = []
    for production in root:
        lhs = AND(parsing(production[0]))
        # lhs.extend(parsing(production[0]))
        rhs = production[1].attrib
        result.append((lhs, rhs))
    return result


def parsing(root):
    out = []
    for cond in root:
        if cond.tag == 'has':
            out.append(Cond(**cond.attrib))
        elif cond.tag == 'neg':
            out.append(Neg(**cond.attrib))
        elif cond.tag == 'filter':
            out.append(Filter(cond.text))
        elif cond.tag == 'bind':
            to = cond.attrib.get('to')
            out.append(Bind(cond.text, V(to)))
        elif cond.tag == 'ncc':
            n = Ncc(parsing(cond))
            out.append(n)
    return out
