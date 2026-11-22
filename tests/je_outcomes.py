"""Select native 1.15 JE outcomes for existing behavioural regression fixtures.

This reads source contracts; it does not emulate native outcome scheduling.
"""
import re

from tools.check_override_inventory import extract_braced_object, top_level_matches


def direct_fields(source):
    inner = source[source.index('{') + 1:source.rfind('}')]
    for match in top_level_matches(re.compile(r'^\s*(\w+)\s*=\s*', re.M), inner):
        start = match.end()
        if inner[start] == '{':
            value = extract_braced_object(inner, start)
        else:
            value = inner[start:].split('\n', 1)[0].split('#', 1)[0].strip()
        yield match.group(1), value


def outcome_block(source, kind):
    matches = []
    for key, value in direct_fields(source):
        if key != 'outcome':
            continue
        fields = dict(direct_fields(value))
        flags = fields.get('flags', '')
        actual = ('invalid' if 'invalid_outcome' in flags else
                  'timeout' if 'timeout' in flags else
                  'complete' if fields.get('color') == '"gold_positive"' else
                  'fail' if fields.get('color') == '"blue_negative"' else None)
        if actual == kind:
            matches.append('outcome = ' + value)
    if len(matches) != 1:
        raise AssertionError(f'expected one {kind} outcome, found {len(matches)}')
    return matches[0]


def outcome_field(source, kind, field):
    value = dict(direct_fields(outcome_block(source, kind))).get(field)
    return field + ' = ' + value if value is not None else ''


def outcome_nodes(nodes, kind):
    matches = []
    for key, _, value in nodes:
        if key != 'outcome':
            continue
        fields = {k: v for k, _, v in value}
        flags = {k for k, _, _ in fields.get('flags', [])}
        actual = ('invalid' if 'invalid_outcome' in flags else
                  'timeout' if 'timeout' in flags else
                  'complete' if fields.get('color') == '"gold_positive"' else
                  'fail' if fields.get('color') == '"blue_negative"' else None)
        if actual == kind:
            matches.append(value)
    if len(matches) != 1:
        raise AssertionError(f'expected one {kind} outcome, found {len(matches)}')
    return matches[0]
