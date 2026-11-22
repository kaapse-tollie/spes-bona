#!/usr/bin/env python3
"""Check 1.15 coastal access and reproduce SB's impassable-coast correction.

Native river-port omissions and actual travel remain engine checks.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_1_15_SHA256 = "7dffae4747c9885a48ec8446931681f2c4b9bd7b4b1ba04984569ef61cc22064"
EXPECTED_1_15_NODE_COUNT = 11010
EXPECTED_1_15_CONNECTION_COUNT = 11091
NETWORK_PATH = Path("common/travel_network/naval_network.txt")
HARBOR_NODE_TYPES = {"harbor", "harbor_from_spline"}
# These exact 1.15 native controls also lack a coastal node. Never exempt an
# altered SB port or geometry, or turn an unexpected native failure into a pass.
NATIVE_ACCESS_PENDING = {"STATE_BENIN", "STATE_BAS_CONGO"}
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
    provinces: tuple[str, ...] = ()
    identifier: int | None = None


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


def impassable_provinces(paths: list[Path]) -> set[str]:
    provinces: set[str] = set()
    for path in paths:
        text = path.read_text(encoding="utf-8-sig")
        for match in re.finditer(r"(?m)^[ \t]*impassable\s*=\s*\{", text):
            opening = text.index("{", match.start())
            body = text[opening + 1:matching_brace(text, opening)]
            body = re.sub(r"(?m)#.*$", "", body)
            provinces.update(normalize_province(p) for p in re.findall(r"x[0-9A-Fa-f]{6}", body))
    return provinces


def prune_impassable_harbours(source: str, impassable: set[str]) -> str:
    """Remove only generated harbour leaves on impassable land; reindex edges.

    Keep native node bodies and connection order. Reject a through route rather
    than silently removing it. Building ports and spline anchors are untouched.
    """
    network = parse_naval_network_text(source)
    removed = {node.index for node in network.nodes
               if node.type == "harbor" and node.province in impassable}
    if not removed:
        return source
    for index in removed:
        neighbors = [b if a == index else a for a, b in network.connections if index in (a, b)]
        if len(neighbors) != 1 or network.nodes[neighbors[0]].type not in {"sea", "sea_from_spline"}:
            raise NavalNetworkError(f"impassable harbour {index} is not a leaf connected to sea; review its route")
    remap = {old: new for new, old in enumerate(i for i in range(len(network.nodes)) if i not in removed)}
    node_block = assignment_block(source, "nodes")
    nodes = flat_record_bodies(node_block, "nodes")
    connection_block = assignment_block(source, "connections")
    connections = []
    for body, (a, b) in zip(flat_record_bodies(connection_block, "connections"), network.connections):
        if a in removed or b in removed:
            continue
        connections.append(re.sub(r"\b(from|to)(\s*=\s*)(\d+)",
                                  lambda m: m[1] + m[2] + str(remap[int(m[3])]), body))
    result = source.replace(node_block, " {" + "} {".join(body for i, body in enumerate(nodes) if i not in removed) + "} ", 1)
    result = result.replace(connection_block, " {" + "} {".join(connections) + "} ", 1)
    parse_naval_network_text(result)  # Reject dangling indices before writing.
    return result


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
                province_match = re.search(r"\bprovinces\s*=\s*\{", block)
                provinces = ()
                if province_match:
                    start = block.index("{", province_match.start())
                    finish = matching_brace(block, start)
                    provinces = tuple(normalize_province(p) for p in re.findall(
                        r"x[0-9A-Fa-f]{6}", block[start:finish]))
                identifier = re.search(r"(?m)^[ \t]*id\s*=\s*(\d+)", block)
                ports.append(StatePort(state, normalize_province(matches[0]), path, provinces,
                                       int(identifier[1]) if identifier else None))
    if not seen_states:
        raise NavalNetworkError("no state blocks found")
    if not ports:
        raise NavalNetworkError("no state ports found")
    return tuple(ports)


def unchanged_native_spline_port(identifier: int | None, current, native) -> bool:
    """Bounded native control for a building port omitted from the cached graph.

    Require both port anchors and an entire direct sea route to be byte-identical
    to native. This proves source preservation, not engine movement.
    """
    if identifier is None:
        return False
    try:
        from tools import spline_structured_merge as spline, repair_launch_spline as repair
    except ModuleNotFoundError:
        import spline_structured_merge as spline
        import repair_launch_spline as repair
    points, original = spline.record_map(current.points), spline.record_map(native.points)
    port = (1 << 23) + identifier * 100
    for anchor in (identifier * 100 + 3, port):
        if anchor not in original or points.get(anchor) != original[anchor]:
            return False
    links, strips = spline.record_map(current.links), spline.record_map(current.strips)
    original_strips = spline.record_map(native.strips)
    for link in native.links:
        ends = set(repair.link_endpoints(link.key))
        # Native sea regions have IDs >= 3000 in this pinned map.
        if link.key & 63 != 3 or port not in ends or not any((1 << 23) + 300000 <= end < (1 << 24) for end in ends):
            continue
        if links.get(link.key) != link:
            continue
        route = [original_strips[key] for key in link.payload]
        if all(strips.get(record.key) == record for record in route) and all(
                points.get(key) == original[key] for record in route for key in record.payload):
            return True
    return False


def validate_state_ports(
    network: NavalNetwork, ports: tuple[StatePort, ...]
) -> tuple[str, ...]:
    by_province: dict[str, list[NavalNode]] = defaultdict(list)
    for node in network.nodes:
        by_province[node.province].append(node)

    # A connected harbour must reach a sea node, not merely another isolated
    # harbour. Separate native sea components remain valid (lakes/straits).
    neighbors: dict[int, set[int]] = defaultdict(set)
    for source, target in network.connections:
        neighbors[source].add(target)
        neighbors[target].add(source)
    sea_reachable = {node.index for node in network.nodes
                     if node.type in {"sea", "sea_from_spline"}}
    pending = list(sea_reachable)
    while pending:
        for neighbor in neighbors[pending.pop()]:
            if neighbor not in sea_reachable:
                sea_reachable.add(neighbor)
                pending.append(neighbor)

    errors: list[str] = []
    for port in ports:
        if port.provinces and port.province not in port.provinces:
            errors.append(f"{port.state} port {port.province} is outside its state region")
            continue
        # 1.15 has coastal-province harbours rather than one generated node at
        # every designated building-port province. This checks state access;
        # it does not certify the engine's building/river/spline route.
        nodes = [node for province in (port.provinces or (port.province,))
                 for node in by_province.get(province, [])]
        harbor_nodes = [node for node in nodes if node.type in HARBOR_NODE_TYPES]
        connected = [node for node in harbor_nodes if node.index in sea_reachable]
        if not nodes:
            errors.append(f"{port.state} port {port.province} has no naval node")
        elif not harbor_nodes:
            kinds = ", ".join(sorted({node.type for node in nodes}))
            errors.append(
                f"{port.state} port {port.province} has no harbor node (types: {kinds})"
            )
        elif not connected:
            errors.append(f"{port.state} port {port.province} harbor has no route to a sea node")
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
        default=EXPECTED_1_15_SHA256,
        help="required upstream naval_network.txt SHA-256",
    )
    parser.add_argument("--write-network", action="store_true",
                        help="rebuild SB's network override from the pinned native file and current impassable provinces")
    args = parser.parse_args()

    game_root = find_game_root(args.game_root)
    if game_root is None:
        parser.error("Victoria 3 game root not found")
    naval_path = game_root / NETWORK_PATH
    if not naval_path.is_file():
        parser.error(f"naval network not found: {naval_path}")
    actual_hash = sha256(naval_path)
    if actual_hash != args.expected_sha256:
        print(
            f"[FAIL] naval network SHA-256: expected {args.expected_sha256}, got {actual_hash}"
        )
        return 1

    try:
        native_source = naval_path.read_text(encoding="utf-8-sig")
        native_network = parse_naval_network_text(native_source)
        state_paths = sorted(args.state_region_root.glob("*.txt"))
        ports = parse_state_ports(state_paths)
        impassable = impassable_provinces(state_paths)
        expected = prune_impassable_harbours(native_source, impassable).encode("utf-8-sig")
        effective_path = ROOT / NETWORK_PATH
        if args.write_network:
            effective_path.parent.mkdir(parents=True, exist_ok=True)
            effective_path.write_bytes(expected)
        if not effective_path.is_file() or effective_path.read_bytes() != expected:
            raise NavalNetworkError("SB network differs from the reviewed native-minus-impassable-harbours derivation")
        network = parse_naval_network(effective_path)
        native_paths = [game_root / "map_data/state_regions" / p.name for p in state_paths]
        native_ports = parse_state_ports([p for p in native_paths if p.is_file()])
        native_by_state = {p.state: p for p in native_ports}
        pending = []
        spline_pending = []
        checked = []
        try:
            from tools import spline_structured_merge as spline
        except ModuleNotFoundError:
            import spline_structured_merge as spline
        spline_path = "gfx/map/spline_network/spline_network.splnet"
        current_spline = spline.parse((ROOT / spline_path).read_bytes())
        native_spline = spline.parse((game_root / spline_path).read_bytes())
        for port in ports:
            native = native_by_state.get(port.state)
            if (native and port.state in NATIVE_ACCESS_PENDING
                    and port.province == native.province
                    and set(port.provinces) == set(native.provinces)
                    and validate_state_ports(native_network, (native,))):
                pending.append(port.state)
            elif (native and port.identifier == native.identifier and port.province == native.province
                  and port.province not in impassable and port.province in port.provinces
                  and validate_state_ports(network, (port,))
                  and unchanged_native_spline_port(port.identifier, current_spline, native_spline)):
                spline_pending.append(port.state)
            else:
                checked.append(port)
        errors = validate_state_ports(network, tuple(checked))
    except (OSError, UnicodeError, NavalNetworkError) as error:
        print(f"[FAIL] naval network validation: {error}")
        return 1

    if errors:
        for error in errors:
            print(f"[FAIL] {error}")
        return 1
    for state in pending:
        print(f"[WARN] {state}: unchanged native port/coast absent from generated graph; river/spline access awaits DP engine verification")
    for state in spline_pending:
        print(f"[WARN] {state}: native building-port anchors and sea route preserved exactly; no generated coastal harbour remains; engine travel pending")
    print(
        "[PASS] naval network: "
        f"{len(network.nodes)} nodes, {len(network.connections)} connections, "
        f"{len(checked)} states with generated coastal access, {len(spline_pending)} unchanged native spline ports, "
        f"{len(pending)} native river cases engine pending"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
