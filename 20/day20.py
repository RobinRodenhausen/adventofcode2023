import itertools
import math


class Module:
    id: str
    _id: str
    is_flipflop: bool
    is_conjunction: bool
    outputs: list[str]
    inputs: dict[str, bool]

    # High/On = True, Low/Off = False
    state: bool

    def __init__(self, line: str) -> None:
        self.is_flipflop = False
        self.is_conjunction = False

        module, destinations = line.split(" -> ")
        self._id = module
        self.outputs = [s.strip() for s in destinations.split(",")]

        if module.startswith("%"):
            self.is_flipflop = True
            self.id = module[1:]
            self.state = False
        elif module.startswith("&"):
            self.is_conjunction = True
            self.id = module[1:]
            self.state = False
            self.inputs = {}
        else:
            self.id = module
            self.state = None  # pyright: ignore[reportGeneralTypeIssues]

    def __str__(self) -> str:
        return f"ID:{self._id} S:{self.state} O:{self.outputs} {'I:' + str(self.inputs) if hasattr(self, 'inputs') else ''}"

    def __expr__(self) -> str:
        return self.__str__()

    def add_input(self, input, state=False):
        if not self.is_conjunction:
            raise ValueError("Input is not needed")
        self.inputs[input] = state


def read_lines() -> list[str]:
    with open("20/input", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


def parse_input() -> dict[str, Module]:
    lines = read_lines()
    modules: dict[str, Module] = {}
    for line in lines:
        m = Module(line)
        modules[m.id] = m

    for k1, v1 in modules.items():
        if v1.is_conjunction:
            for k2, v2 in modules.items():
                if k1 in v2.outputs:
                    v1.add_input(k2)

    # Debug
    # for km, vm in modules.items():
    #     print(vm)

    return modules


def part1():
    modules = parse_input()

    low = 0
    high = 0

    # current, signal(low/high), last
    queue: list[tuple[str, bool, str]]
    for i in range(1000):
        # Button press
        queue = [("broadcaster", False, "")]
        while queue:
            (current, signal, last_module) = queue.pop(0)
            if signal:
                high += 1
            else:
                low += 1

            if current not in modules:
                # Reached output
                # print(f"Invalid target {current}")
                continue

            module = modules[current]
            # is Flipflop
            if module.is_flipflop:
                # and recives low pulse (high is ignored)
                if not signal:
                    # Flip state
                    module.state = not module.state
                    # Send flipped state to outputs
                    for output in module.outputs:
                        queue.append((output, module.state, current))
            elif module.is_conjunction:
                module.inputs[last_module] = signal
                # If all inputs are high send low
                if all(module.inputs.values()):
                    signal = False
                # otherwise send high
                else:
                    signal = True
                # Send signal to all outputs
                for output in module.outputs:
                    queue.append((output, signal, current))
            # Should only be triggered by broadcaster
            else:
                if current != "broadcaster":
                    raise ValueError(f"{current} should not follow this path")
                for output in module.outputs:
                    queue.append((output, signal, current))

    total = low * high
    print(f"Total 1: {total}")
    assert total == 11687500 or total == 681194780


def part2():
    modules = parse_input()

    # There is only one rx in the input data and follows after &bq
    # print(modules["bq"].inputs)
    # which has 4 inputs &vg, &kp, &gc, &tx
    # each one has to receive a low signal in the same cycle to send a high signal to bq

    direct_parents: dict[str, int] = {}

    for key in modules["bq"].inputs.keys():
        direct_parents[key] = None  # pyright: ignore[reportGeneralTypeIssues]

    queue: list[tuple[str, bool, str]]
    for i in itertools.count(1):
        # if i % 10000 == 0:
        #     print(i)

        # Collect at which cycle the direct parents send a high signal (recive a low signal)
        if all(v is not None for v in direct_parents.values()):
            break

        queue = [("broadcaster", False, "")]
        while queue:
            (current, signal, last_module) = queue.pop(0)

            # Get the first occurance of a low signal for each direct parent
            if current in direct_parents and not signal:
                direct_parents[current] = i

            # brute force. May take a while to get to 238593356738827...
            if current == "rx" and not signal:
                print(i)
                print("RX:", signal)

            if current not in modules:
                continue

            module = modules[current]
            # is Flipflop
            if module.is_flipflop:
                # and recives low pulse (high is ignored)
                if not signal:
                    # Flip state
                    module.state = not module.state
                    # Send flipped state to outputs
                    for output in module.outputs:
                        queue.append((output, module.state, current))
            elif module.is_conjunction:
                module.inputs[last_module] = signal
                # If all inputs are high send low
                if all(module.inputs.values()):
                    signal = False
                # otherwise send high
                else:
                    signal = True
                # Send signal to all outputs
                for output in module.outputs:
                    queue.append((output, signal, current))
            # Should only be triggered by broadcaster
            else:
                if current != "broadcaster":
                    raise ValueError(f"{current} should not follow this path")
                for output in module.outputs:
                    queue.append((output, signal, current))

    # print(direct_parents)
    # {'vg': 4027, 'kp': 3929, 'gc': 4001, 'tx': 3769}
    # Get the least common multiple when the cycles match which in my case is vg*kp*gc*tx
    total = math.lcm(*list(direct_parents.values()))
    print(f"Total 2: {total}")
    # 238.593.356.738.827
    # So someone has to press the button over 238 trillion times?
    assert total == 238593356738827


if __name__ == "__main__":
    part1()
    part2()
