import re

from solution import Solutions

Data = list[str]


def parse_input(lines: list[str]) -> Data:
    return lines[0].strip().split(",")


def hasher(s: str):
    val = 0
    for c in s:
        val += ord(c)
        val *= 17
        val %= 256
    return val


def part_1(data: Data):
    return sum(hasher(s) for s in data)


def part_2(data: Data):
    boxes = {idx: [] for idx in range(256)}

    for chunk in data:
        label, operation = re.match(r"^(\w+)([=-])", chunk).groups()

        box_id = hasher(label)
        box = boxes[box_id]

        if operation == "-":
            for item in box:
                lens_label = item[0]
                if lens_label == label:
                    box.remove(item)
                    break
        if operation == "=":
            # adding a label
            focal_length = int(chunk[-1])
            for idx, (lens_label, _) in enumerate(box):
                if lens_label == label:
                    box[idx] = (label, focal_length)
                    break
            else:
                # clean exit, so item is not in the box
                box.append((label, focal_length))

    focusing_power = 0
    for box_idx in range(256):
        focusing_power += sum(
            (box_idx + 1) * (lens_idx + 1) * focal_length
            for lens_idx, (_, focal_length) in enumerate(boxes[box_idx])
        )

    return focusing_power


SOLUTION = Solutions(
    day=15,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=506891,
    part_2_answer=230462,
)


class Tests:
    DATA = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7".split("\n")

    def test_hasher(self):
        assert hasher("rn=1") == 30

    def test_part_1(self):
        assert part_1(parse_input(self.DATA)) == 1320

    def test_part_2(self):
        assert part_2(parse_input(self.DATA)) == 145

    def test_part_2_values(self):
        assert SOLUTION.part_2() > 57243


if __name__ == "__main__":
    print(SOLUTION.part_1())
    print(SOLUTION.part_2())
