from dataclasses import dataclass,field

@dataclass
class C(): # generic container
    val:int = 0

@dataclass
class Buffer():
    rp: int = 0
    wp: int = 0
    len: int = 0
    rep: list[int] = field(default_factory=list)

    # temporally
    def __post_init__(self):
        if len(self.rep) == 0:
            self.rep = [0] * 10
        self.len = len(self.rep)

    def put(self,v):
        self.rep[self.wp] = v
        self.wp += 1 # TODO adjust

    def get(self):
        v = self.rep[self.rp]
        self.rp += 1 # TODO adjust
        return v

# usage
def main():
    c = C(0)
    print(f"c={c}")
    c.val = "abc"
    print(f"c={c}")
    b1 = Buffer()
    print(f"b1={b1}")
    b2 = Buffer()
    print(f"b2={b2}")
    b1.rep = [1, 2, 3] # illegal
    print(f"b1={b1}")
    print(f"b2={b2}")

if __name__ == '__main__':
    main()
