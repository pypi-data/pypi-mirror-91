import unittest
import bnk


class SpaceTest(unittest.TestCase):
    def test0_space_repr0_unnamed(self):
        space = bnk.NumSpace(3)
        print(space)

    def test0_space_repr1_named(self):
        space = bnk.NumSpace(3, 'n')
        print(space)

    def test1_ket_space_repr(self):
        space = bnk.KetSpace(3)
        print(space)

    def test2_bra_space_eq(self):
        ket_space = bnk.KetSpace(3)
        bra_space = ket_space.ct
        bra_space2 = bnk.BraSpace(ket_space)

        self.assertTrue(hash(bra_space) == hash(bra_space2), "hash does not equals")
        self.assertTrue(bra_space == bra_space2, "object does not equals")
