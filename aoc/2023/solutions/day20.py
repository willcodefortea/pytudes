import math
from collections import defaultdict
from typing import Callable, Generator

from solution import Solutions

HI = True
LO = False
Signal = bool
Module = Generator[tuple[str, Signal], None, None]
Graph = dict[str, list[str]]
ModuleGraph = dict[str, Callable[[Signal, str], Module]]
Data = tuple[ModuleGraph, Graph]


def build_filp_flop(destinations: list[str]):
    is_on = False

    def run(signal: Signal, _: str):
        nonlocal is_on
        if signal == HI:
            return
        signal = LO if is_on else HI
        is_on = not is_on

        for module in destinations:
            yield module, signal

    def reset():
        nonlocal is_on
        is_on = False

    run.reset = reset

    return run


def build_conjunction(destinations: list[str], modules: list[str]):
    states = {actor: False for actor in modules}

    def run(signal: Signal, module: str):
        nonlocal states
        states[module] = signal
        out_signal = LO if all(states.values()) else HI
        for module in destinations:
            yield module, out_signal

    def reset():
        nonlocal states
        states = {actor: False for actor in modules}

    run.reset = reset

    return run


def build_broadcast(destinations: list[str]):
    def run(signal: Signal, module: str):
        for mod in destinations:
            yield mod, signal

    def reset():
        pass

    run.reset = reset
    return run


def parse_input(lines: list[str]) -> Data:
    graph: dict[str, list[str]] = {}
    modules: ModuleGraph = {}

    conjunctions = []
    targets = defaultdict(list)

    for line in lines:
        if not line:
            continue

        name, all_destinations = line.split(" -> ")
        destinations = [d.strip() for d in all_destinations.split(",")]
        module_name = name[1:] if name.startswith("%") or name.startswith("&") else name
        graph[module_name] = destinations

        for dest in destinations:
            targets[dest].append(module_name)

        if name.startswith("%"):
            modules[module_name] = build_filp_flop(destinations)
        elif name.startswith("&"):
            conjunctions.append((module_name, destinations))
        elif name == "broadcaster":
            modules[module_name] = build_broadcast(destinations)

    for name, destinations in conjunctions:
        modules[name] = build_conjunction(destinations, targets[name])

    for key in targets:
        if key not in modules:
            # weird output state, just treat as an empty broadcaster
            modules[key] = build_broadcast([])

    return modules, graph


def run_loop(modules: Data, queue: list[tuple[str, Signal, str]]):
    sent_signals = [queue[0]]
    while queue:
        module, signal, origin = queue.pop(0)
        for destination, out_signal in modules[module](signal, origin):
            queue.append((destination, out_signal, module))
            sent_signals.append((destination, out_signal, module))
    return sent_signals


def push_button(modules: Data):
    queue: list[tuple[str, Signal, str]] = [
        ("broadcaster", LO, "button"),
    ]
    return run_loop(modules, queue)


def part_1(data: Data) -> int:
    module_graph = data[0]
    lo_count = 0
    hi_count = 0
    for _ in range(1000):
        signals = push_button(module_graph)
        lo_count += sum(not s for _, s, _ in signals)
        hi_count += sum(s for _, s, _ in signals)
    return lo_count * hi_count


def part_2(data: Data) -> int:
    modules, graph = data
    for mod in modules.values():
        mod.reset()

    # find the conjunction node that points to our destination, rx
    conjunction_node = None
    for node, targets in graph.items():
        if "rx" in targets:
            conjunction_node = node
            break
    assert conjunction_node, "Unable to find conjunction"

    # now find all nodes that point to this conjunction, they all need to send
    # a HI pulse at the same time
    first_hi_pulse = {}
    for node, targets in graph.items():
        if conjunction_node in targets:
            first_hi_pulse[node] = -1

    # press the button and track when the feeders send their first LO pulse
    loop_count = 0
    finished = False
    while not finished:
        signals = push_button(modules)
        loop_count += 1
        for mod, sig, feeder in signals:
            if mod == conjunction_node and sig == HI:
                first_hi_pulse[feeder] = loop_count
                finished = all(v != -1 for v in first_hi_pulse.values())

    # then the answer is the first time they all send a HI pulse!
    return math.lcm(*first_hi_pulse.values())


SOLUTION = Solutions(
    day=20,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=898557000,
    part_2_answer=238420328103151,
)


class Test:
    DATA_SIMPLE = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a""".split(
        "\n"
    )
    DATA = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output""".split(
        "\n"
    )

    def test_flip_flop(self):
        flip_flop = build_filp_flop(["bar"])
        assert list(flip_flop(HI, "")) == []
        # was off, turning on
        assert list(flip_flop(LO, "")) == [("bar", True)]
        assert list(flip_flop(HI, "")) == []
        # was on, turning off
        assert list(flip_flop(LO, "")) == [("bar", False)]

    def test_part_1(self):
        assert part_1(parse_input(self.DATA_SIMPLE)) == 32000000

    def test_part_2(self):
        assert SOLUTION.part_2() > 431481152760
        assert False


if __name__ == "__main__":
    print(SOLUTION.part_1())
    print(SOLUTION.part_2())
