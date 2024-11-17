from ..utils.Buffer import *

class Acquire():

    def m11e(self, cur: int, dvk: int, svk: int, svkc: C):
        if dvk == 0:
            return -1
        if cur % dvk == 0:
            svkc.val = svk
        return 0

    def m12e(self, cur: int, svk: int, wvk: tuple[int, int, int, int], avkc: C):
        sv_lb,sv_ub,av_lb,av_ub = wvk
        if sv_ub<sv_lb:
            return -1
        if svk<sv_lb:
            avkc.val = av_lb
        if sv_ub<svk:
            avkc.val = av_ub
        return 0

    # temporally
    def m11(self, t: int, dv: tuple[int, int], sv: list[int], svc: list[int]):
        svkc = C(0)
        for k,dvk in enumerate(dv):
            svkc.val = svc[k]
            self.m11e(t, dvk, sv[k], svkc)
            svc[k] = svkc.val

    def m12(self,t: int, wv: list[tuple[int, int, int, int]], sv: list[int], avc: list[int]):
        avkc = C(0)
        for k in range(4):
            avkc.val = avc[k]
            self.m12e(t, sv[k], wv[k], avkc)
            avc[k] = avkc.val

    # must be defined out of the functions
    svc = [0, 0, 0, 0]
    avc = [0, 0, 0, 0]

    def run(self, t):
        dv = [2,3,4,5]
        wv = [
            ( 50,150,10,-10),
            (150,250,20,-20),
            (250,350,30,-30),
            (350,450,40,-40)
        ]
        sv = [100 + t * 44, 200 + t * 33, 300 + t * 22, 400 + t * 11]
        self.m11(t, dv, sv, self.svc)
        print(f"t={t} svc={self.svc} ",end='')
        self.m12(t, self.svc, wv, self.avc)
        print(f"avc={self.avc}")

    def main(self):
        for cur in range(0,6):
            self.run(cur)
