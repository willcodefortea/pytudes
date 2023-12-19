import operator
import re
from functools import partial
from typing import Callable

from solution import Solutions

State = dict[str, int]
Rules = dict[str, Callable[[State], bool]]
Data = tuple[Rules, list[State]]


def parse_input(lines: list[str]) -> Data:
    rules = {"A": [lambda _: True], "R": [lambda _: False]}
    inputs = []

    def root(state, key):
        for rule in rules[key][1:]:
            valid, next_rule = rule(state)
            if not next_rule:
                return valid
            if valid:
                return rules[next_rule][0](state)

    def eval(x, key, op, val, n):
        return op(x[key], val), n

    for line in lines:
        if not line:
            continue

        instruction = re.match(r"(\w+)\{(.+)\}", line)
        if instruction:
            rule_name, ins = instruction.groups()
            rules[rule_name] = []
            rules[rule_name].append(partial(root, key=rule_name))

            for chunk in ins.split(","):
                if chunk == "A":
                    r = lambda _: (True, "")
                elif chunk == "R":
                    r = lambda _: (False, "")
                else:
                    parsed = re.match(r"(\w)(.)(\d+):(\w+)", chunk)
                    if parsed:
                        input, op_s, val, next = parsed.groups()
                        op = operator.lt if op_s == "<" else operator.gt

                        r = partial(eval, key=input, op=op, val=int(val), n=next)
                    else:
                        # simple jump
                        r = partial(eval, key="a", op=operator.gt, val=0, n=chunk)

                rules[rule_name].append(r)
        else:
            chunks = line[1:-1].split(",")
            state = {}
            for chunk in chunks:
                a, b = chunk.split("=")
                state[a] = int(b)
            inputs.append(state)
    return rules, inputs


def part_1(data: Data):
    rules, inputs = data

    res = 0
    for state in inputs:
        root = rules["in"][0]
        accepted = root(state)
        if accepted:
            res += sum(state.values())
    return res


def part_2(data: Data):
    return 0


SOLUTION = Solutions(
    day=19,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=397134,
    part_2_answer=-1,
)


class Tests:
    DATA = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}""".split(
        "\n"
    )

    def test_part_1(self):
        assert part_1(parse_input(self.DATA)) == 19114

    def test_part_2(self):
        assert part_2(parse_input(self.DATA)) == 167409079868000


if __name__ == "__main__":
    print(SOLUTION.part_1())
    print(SOLUTION.part_2())
