#!/usr/bin/env python3
"""Validate Spes Bona state ports against Victoria 3's generated naval network."""
from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_OB1_SHA256 = "bca18518598f55d7f1b2b07d04ed88e8389d4db807fa49bdcd53d8bc48ca061f"
EXPECTED_OB1_NODE_COUNT = 6641
EXPECTED_OB1_CONNECTION_COUNT = 7191
HARBOR_NODE_TYPES = {"harbor", "harbor_from_spline"}
STATE_RE = re.compile(r"^(STATE_[A-Z0-9_]+)\s*=\s*\{", re.MULTILINE)
ASSIGNMENT_RE = re.compile(
    r'([A-Za-z_][A-Za-z0-9_]*)\s*=\s*("(?:[^"\\]|\\.)*"|[^\s{}]+)'
)


class NavalNetworkError(ValueError):
    pass


@dataclass(frozen=True)
class NavalNode:
    index: int
    province: str
    x: int
    y: int
    type: str


@dataclass(frozen=True)
class NavalNetwork:
    nodes: tuple[NavalNode, ...]
    connections: tuple[tuple[int, int], ...]
    degrees: tuple[int, ...]

    def nodes_for_province(self, province: str) -> tuple[NavalNode, ...]:
        normalized = normalize_province(province)
        return tuple(node for node in self.nodes if node.province == normalized)


@dataclass(frozen=True)
class StatePort:
    state: str
    province: str
    source: Path


def normalize_province(value: str) -> str:
    if not re.fullmatch(r"x[0-9A-Fa-f]{6}", value):
        raise NavalNetworkError(f"invalid province ID: {value}")
    return "x" + value[1:].upper()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matching_brace(text: str, open_index: int) -> int:
    if open_index >= len(text) or text[open_index] != "{":
        raise NavalNetworkError(f"expected opening brace at offset {open_index}")
    depth = 0
    quoted = False
    escaped = False
    comment = False
    for index in range(open_index, len(text)):
        character = text[index]
        if comment:
            if character == "\n":
                comment = False
            continue
        if quoted:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quoted = False
            continue
        if character == "#":
            comment = True
        elif character == '"':
            quoted = True
        elif character == "{":
            depth += 1
        elif character == "}":
            depth -= 1
            if depth == 0:
                return index
            if depth < 0:
                break
    raise NavalNetworkError(f"unclosed brace at offset {open_index}")


def brace_delta(line: str) -> int:
    """Count structural braces on one line, ignoring quotes and comments."""
    delta = 0
    quoted = False
    escaped = False
    for character in line:
        if quoted:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quoted = False
            continue
        if character == "#":
            break
        if character == '"':
            quoted = True
        elif character == "{":
            delta += 1
        elif character == "}":
            delta -= 1
    return delta


def depth_zero_port_values(state_block: str) -> tuple[str, ...]:
    """Return only direct state `port` fields, never nested assignments."""
    port_re = re.compile(
        r'^\s*port\s*=\s*"?(x[0-9A-Fa-f]{6})"?\s*(?:#.*)?$'
    )
    depth = 0
    result: list[str] = []
    for line in state_block.splitlines():
        if depth == 0:
            match = port_re.fullmatch(line)
            if match:
                result.append(match.group(1))
        depth += brace_delta(line)
        if depth < 0:
            raise NavalNetworkError("state block has an unmatched closing brace")
    if depth != 0:
        raise NavalNetworkError("state block has unclosed nested braces")
    return tuple(result)


def assignment_block(text: str, name: str) -> str:
    matches = list(re.finditer(rf"(?m)^\s*{re.escape(name)}\s*=\s*\{{", text))
    if len(matches) != 1:
        raise NavalNetworkError(f"expected exactly one {name} block, found {len(matches)}")
    opening = text.find("{", matches[0].start(), matches[0].end())
    closing = matching_brace(text, opening)
    return text[opening + 1 : closing]


def only_whitespace_or_comments(text: str) -> bool:
    return not re.sub(r"(?m)#.*$", "", text).strip()


def flat_record_bodies(block: str, context: str) -> tuple[str, ...]:
    records: list[str] = []
    position = 0
    while position < len(block):
        while position < len(block):
            if block[position].isspace():
                position += 1
                continue
            if block[position] == "#":
                newline = block.find("\n", position)
                position = len(block) if newline < 0 else newline + 1
                continue
            break
        if position >= len(block):
            break
        if block[position] != "{":
            preview = block[position : position + 40].splitlines()[0]
            raise NavalNetworkError(
                f"unexpected content in {context} at offset {position}: {preview!r}"
            )
        closing = matching_brace(block, position)
        body = block[position + 1 : closing]
        if "{" in re.sub(r'"(?:[^"\\]|\\.)*"', "", body):
            raise NavalNetworkError(f"nested record in {context} at offset {position}")
        records.append(body)
        position = closing + 1
    return tuple(records)


def parse_assignments(body: str, expected: set[str], context: str) -> dict[str, str]:
    values: dict[str, str] = {}
    cursor = 0
    for match in ASSIGNMENT_RE.finditer(body):
        if not only_whitespace_or_comments(body[cursor : match.start()]):
            raise NavalNetworkError(
                f"malformed {context} record near {body[cursor:match.start()]!r}"
            )
        key, value = match.groups()
        if key in values:
            raise NavalNetworkError(f"duplicate {key} in {context} record")
        values[key] = value[1:-1] if value.startswith('"') else value
        cursor = match.end()
    if not only_whitespace_or_comments(body[cursor:]):
        raise NavalNetworkError(f"malformed trailing content in {context} record")
    if set(values) != expected:
        raise NavalNetworkError(
            f"{context} record fields must be {sorted(expected)}, got {sorted(values)}"
        )
    return values


def parse_naval_network_text(text: str) -> NavalNetwork:
    node_records = flat_record_bodies(assignment_block(text, "nodes"), "nodes")
    connection_records = flat_record_bodies(
        assignment_block(text, "connections"), "connections"
    )
    if not node_records:
        raise NavalNetworkError("naval network has no nodes")

    nodes: list[NavalNode] = []
    for index, body in enumerate(node_records):
        values = parse_assignments(body, {"province", "x", "y", "type"}, "node")
        try:
            x = int(values["x"])
            y = int(values["y"])
        except ValueError as error:
            raise NavalNetworkError(f"node {index} has a non-integer coordinate") from error
        nodes.append(
            NavalNode(
                index=index,
                province=normalize_province(values["province"]),
                x=x,
                y=y,
                type=values["type"],
            )
        )

    connections: list[tuple[int, int]] = []
    degrees = [0] * len(nodes)
    for index, body in enumerate(connection_records):
        values = parse_assignments(body, {"from", "to"}, "connection")
        try:
            source = int(values["from"])
            target = int(values["to"])
        except ValueError as error:
            raise NavalNetworkError(f"connection {index} has a non-integer endpoint") from error
        if not 0 <= source < len(nodes) or not 0 <= target < len(nodes):
            raise NavalNetworkError(
                f"connection {index} endpoint outside 0..{len(nodes) - 1}: {source}, {target}"
            )
        connections.append((source, target))
        degrees[source] += 1
        degrees[target] += 1

    return NavalNetwork(tuple(nodes), tuple(connections), tuple(degrees))


def parse_naval_network(path: Path) -> NavalNetwork:
    return parse_naval_network_text(path.read_text(encoding="utf-8-sig"))


def parse_state_ports(paths: list[Path]) -> tuple[StatePort, ...]:
    ports: list[StatePort] = []
    seen_states: dict[str, Path] = {}
    for path in sorted(paths):
        text = path.read_text(encoding="utf-8-sig")
        for match in STATE_RE.finditer(text):
            state = match.group(1)
            if state in seen_states:
                raise NavalNetworkError(
                    f"duplicate state {state} in {seen_states[state]} and {path}"
                )
            seen_states[state] = path
            opening = text.find("{", match.start(), match.end())
            closing = matching_brace(text, opening)
            block = text[opening + 1 : closing]
            matches = depth_zero_port_values(block)
            if len(matches) > 1:
                raise NavalNetworkError(f"state {state} has multiple port fields")
            if matches:
                ports.append(StatePort(state, normalize_province(matches[0]), path))
    if not seen_states:
        raise NavalNetworkError("no state blocks found")
    if not ports:
        raise NavalNetworkError("no state ports found")
    return tuple(ports)


def validate_state_ports(
    network: NavalNetwork, ports: tuple[StatePort, ...]
) -> tuple[str, ...]:
    by_province: dict[str, list[NavalNode]] = defaultdict(list)
    for node in network.nodes:
        by_province[node.province].append(node)

    errors: list[str] = []
    for port in ports:
        nodes = by_province.get(port.province, [])
        harbor_nodes = [node for node in nodes if node.type in HARBOR_NODE_TYPES]
        connected = [node for node in harbor_nodes if network.degrees[node.index] > 0]
        if not nodes:
            errors.append(f"{port.state} port {port.province} has no naval node")
        elif not harbor_nodes:
            kinds = ", ".join(sorted({node.type for node in nodes}))
            errors.append(
                f"{port.state} port {port.province} has no harbor node (types: {kinds})"
            )
        elif not connected:
            errors.append(f"{port.state} port {port.province} harbor node has degree 0")
    return tuple(errors)


def find_game_root(explicit: str | None) -> Path | None:
    candidates = [
        Path(explicit).expanduser() if explicit else None,
        Path(os.environ["VIC3_GAME_ROOT"]).expanduser()
        if os.environ.get("VIC3_GAME_ROOT")
        else None,
        Path.home()
        / "Library/Application Support/Steam/steamapps/common/Victoria 3/game",
        Path.home() / ".local/share/Steam/steamapps/common/Victoria 3/game",
    ]
    return next(
        (path.resolve() for path in candidates if path and (path / "common").is_dir()),
        None,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game-root", help="Victoria 3 game directory")
    parser.add_argument(
        "--state-region-root",
        type=Path,
        default=ROOT / "map_data/state_regions",
        help="directory containing SB state-region files",
    )
    parser.add_argument(
        "--expected-sha256",
        default=EXPECTED_OB1_SHA256,
        help="required naval_network.txt SHA-256",
    )
    args = parser.parse_args()

    game_root = find_game_root(args.game_root)
    if game_root is None:
        parser.error("Victoria 3 game root not found")
    naval_path = game_root / "common/travel_network/naval_network.txt"
    if not naval_path.is_file():
        parser.error(f"naval network not found: {naval_path}")
    actual_hash = sha256(naval_path)
    if actual_hash != args.expected_sha256:
        print(
            f"[FAIL] naval network SHA-256: expected {args.expected_sha256}, got {actual_hash}"
        )
        return 1

    try:
        network = parse_naval_network(naval_path)
        state_paths = sorted(args.state_region_root.glob("*.txt"))
        ports = parse_state_ports(state_paths)
        errors = validate_state_ports(network, ports)
    except (OSError, UnicodeError, NavalNetworkError) as error:
        print(f"[FAIL] naval network validation: {error}")
        return 1

    if errors:
        for error in errors:
            print(f"[FAIL] {error}")
        return 1
    print(
        "[PASS] naval network: "
        f"{len(network.nodes)} nodes, {len(network.connections)} connections, "
        f"{len(ports)} connected SB state ports"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
