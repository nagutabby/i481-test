import pytest # type: ignore[import-not-found]

from src.acquire import *

class TestAcquire():
    @pytest.fixture()
    def trace(self, **args):
        # setup
        print(f"\nsetup :")
        yield
        # teardown
        print(f"\nteardown :")

    acq = Acquire()

    @pytest.mark.parametrize("cur, dvk, svk, initial_svkc, expected_svkc, expected_return", [
        # Case 1: Invalid divisor (dvk=0)
        (1, 0, 100, 0, 0, -1),

        # Case 2: Not divisible (cur=1, dvk=2)
        (1, 2, 100, 0, 0, 0),

        # Case 3: Divisible (cur=2, dvk=2) - svkc should be set to svk
        (2, 2, 100, 0, 100, 0),
    ])
    def test_m11e(self, cur, dvk, svk, initial_svkc, expected_svkc, expected_return):
        # Setup
        svkc = C(initial_svkc)

        # Exercise
        result = self.acq.m11e(cur, dvk, svk, svkc)

        # Verify
        assert result == expected_return, \
            f"Expected return value {expected_return}, but got {result}"
        assert svkc.val == expected_svkc, \
            f"Expected svkc.val to be {expected_svkc}, but got {svkc.val}"

    @pytest.mark.parametrize("cur, svk, wvk, initial_avkc, expected_avkc, expected_return", [
        # Case 1: Invalid bounds (sv_ub < sv_lb)
        (1, 150, (200, 100, 100, -100), 0, 0, -1),

        # Case 2: Value below lower bound
        (1, 99, (100, 200, -100, 100), 0, -100, 0),

        # Case 3: Value above upper bound
        (1, 201, (100, 200, -100, 100), 0, 100, 0),
    ])
    def test_m12e(self, cur, svk, wvk, initial_avkc, expected_avkc, expected_return):
        avkc = C(initial_avkc)

        result = self.acq.m12e(cur, svk, wvk, avkc)

        assert result == expected_return, \
            f"Expected return value {expected_return}, but got {result}"
        assert avkc.val == expected_avkc, \
            f"Expected avkc.val to be {expected_avkc}, but got {avkc.val}"

    def test_m11_m11e_error(self):
        t = 2
        dv = (0, 4)
        sv = [100, 200]
        svc = [0, 0]

        self.acq.m11(t, dv, sv, svc)

        assert svc == [0, 0]

    def test_m11_m11e_normal(self):
        t = 2
        dv = (2, 4)
        sv = [100, 200]
        svc = [0, 0]

        self.acq.m11(t, dv, sv, svc)

        assert svc == [100, 0]

    def test_m12_m12e_error(self):
        t = 1
        sv = [100, 200, 300, 400]
        wv = [
            (150, 50, 10, -10),    # Invalid bounds: sv_ub(50) < sv_lb(150)
            (150, 250, 20, -20),   # Valid bounds
            (250, 350, 30, -30),   # Valid bounds
            (450, 350, 40, -40)    # Invalid bounds: sv_ub(350) < sv_lb(450)
        ]
        avc = [0, 0, 0, 0]

        self.acq.m12(t, wv, sv, avc)

        assert avc == [0, 0, 0, 0], "avc values should remain unchanged for invalid bounds"

    def test_m12_m12e_normal(self):
        t = 1
        sv = [40, 260, 300, 460]  # 範囲外、範囲外、範囲内、範囲外の値を設定
        wv = [
            (50, 150, 10, -10),   # sv[0]=40 < sv_lb=50 -> av_lb=10
            (150, 250, 20, -20),  # sv_ub=250 < sv[1]=260 -> av_ub=-20
            (250, 350, 30, -30),  # sv_lb=250 <= sv[2]=300 <= sv_ub=350 -> 変化なし(0)
            (350, 450, 40, -40)   # sv_ub=450 < sv[3]=460 -> av_ub=-40
        ]
        avc = [0, 0, 0, 0]

        self.acq.m12(t, wv, sv, avc)

        expected_avc = [10, -20, 0, -40]
        assert avc == expected_avc, f"Expected {expected_avc}, but got {avc}"

    def test_m11_m12_error(self):
        t = 4
        dv = (0, 3, 4, 5)  # First element is invalid (zero)
        sv = [200, 300, 400, 500]
        wv = [
            (150, 50, -100, 100),  # Invalid bounds (sv_ub < sv_lb)
            (150, 250, -200, 200),
            (250, 350, -300, 300),
            (350, 450, -400, 400)
        ]

        svc = [0, 0, 0, 0]
        avc = [0, 0, 0, 0]

        self.acq.m11(t, dv, sv, svc)
        # t=4の場合:
        # dv[0]=0: 無効な値 → 0
        # dv[1]=3: 4÷3=1余り1 → 0
        # dv[2]=4: 4÷4=1余り0 → sv[2]=400
        # dv[3]=5: 4÷5=0余り4 → 0
        self.acq.m12(t, wv, svc, avc)

        expected_svc = [0, 0, 400, 0]
        # svc[0]=0 は < 150 だが、wvの範囲指定が無効なため変化なし → 0
        # svc[1]=0 は < 150 なので av_lb=-200
        # svc[2]=400 は > 350 なので av_ub=300
        # svc[3]=0 は < 350 なので av_lb=-400
        expected_avc = [0, -200, 300, -400]

        assert svc == expected_svc, f"Expected svc={expected_svc}, but got {svc}"
        assert avc == expected_avc, f"Expected avc={expected_avc}, but got {avc}"

    def test_m11_m12_normal(self):
        t = 4
        dv = (2, 3, 4, 5)
        sv = [200, 300, 400, 500]
        wv = [
            (50, 150, -100, 100),
            (150, 250, -200, 200),
            (250, 350, -300, 300),
            (350, 450, -400, 400)
        ]

        svc = [0, 0, 0, 0]
        avc = [0, 0, 0, 0]

        self.acq.m11(t, dv, sv, svc)
        # t=4の場合:
        # dv[0]=2: 4÷2=2余り0 → sv[0]=200
        # dv[1]=3: 4÷3=1余り1 → 0
        # dv[2]=4: 4÷4=1余り0 → sv[2]=400
        # dv[3]=5: 4÷5=0余り4 → 0
        self.acq.m12(t, wv, svc, avc)

        expected_svc = [200, 0, 400, 0]
        # svc[0]=200 は > 150 なので av_ub=100
        # svc[1]=0 は < 150 なので av_lb=-200
        # svc[2]=400 は > 350 なので av_ub=300
        # svc[3]=0 は < 350 なので av_lb=-400
        expected_avc = [100, -200, 300, -400]

        assert svc == expected_svc, f"Expected svc={expected_svc}, but got {svc}"
        assert avc == expected_avc, f"Expected avc={expected_avc}, but got {avc}"
