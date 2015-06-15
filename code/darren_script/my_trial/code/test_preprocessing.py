# -*- coding: utf-8 -*-

from __future__ import division

import numpy as np
import tempfile
import unittest

import align_instances
import augment_with_products
import text_mtx_rw

class PreprocesingTest(unittest.TestCase):
    
    def test_text_mtx_rw(self):
        data = np.reshape(np.arange(5 * 3), (5, 3));
        attrs = ["A", "B", "C"]
        insts = ["1", "2", "3", "4", "5"]
        # Ideally we would refactor text_mtx_rw to take file handles so that
        # we can use in-memory files, but this is good enough for this setting
        tmpfile = tempfile.NamedTemporaryFile(delete=False)
        text_mtx_rw.write_mtx_info(tmpfile.name, data, attrs, insts)
        (read_data, read_attrs, read_insts) = text_mtx_rw.read_mtx_info(tmpfile.name)
        self.assertTrue(np.all(data == read_data))
        self.assertEqual(attrs, read_attrs)
        self.assertEqual(insts, read_insts)

    def test_align_instances(self):
        insts1 = ["inst_1", "inst_2", "inst_3", "inst_4", "inst_5"]
        insts2 = ["inst_4", "inst_6", "inst_1", "inst_7", "inst_5", "inst_8"]
        data1 = np.array([[10, 11], [20, 21], [30, 31], [40, 41], [50, 51]])
        data2 = np.array([[42, 43], [62, 63], [12, 13], [72, 73], [52, 53], [82, 83]])
        expected_insts = ["inst_1", "inst_4", "inst_5"]
        expected_data1 = data1[[0,3,4],:]
        expected_data2 = data2[[2,0,4],:]
        (algn_data1, algn_insts1, algn_data2, algn_insts2) = (
            align_instances.align_instances(data1, insts1, data2, insts2))
        self.assertTrue(np.all(expected_insts == algn_insts1))
        self.assertTrue(np.all(expected_insts == algn_insts2))
        self.assertTrue(np.all(expected_data1 == algn_data1))
        self.assertTrue(np.all(expected_data2 == algn_data2))
        
    def test_augment_with_combinations(self):
        data = np.reshape(np.arange(10*5), (10, 5))
        attrs = ["A", "B", "C", "D", "E"]
        insts = ["inst_{0}".format(i) for i in range(10)]
        
        expected_aug_data = np.hstack(
            (data, 
             np.transpose(np.atleast_2d(data[:,2] * data[:,1])), 
             np.transpose(np.atleast_2d(data[:,2] * data[:,4]))))
        expected_aug_attrs = attrs + ["CxB", "CxE"]
        expected_aug_insts = insts
        (aug_data, aug_attrs, aug_insts) = (
            augment_with_products._augment_with_combinations(
                data, attrs, insts, ["C"], ["B", "E"], 
                fxn=lambda x,y: x*y, fxn_symb='x'))
        self.assertTrue(np.all(aug_data == expected_aug_data))
        self.assertEqual(expected_aug_attrs, aug_attrs)
        self.assertEqual(expected_aug_insts, aug_insts)
        
        expected_aug_data = np.hstack(
            (expected_aug_data, 
             np.transpose(np.atleast_2d(aug_data[:,6] / aug_data[:, 3]))))
        expected_aug_attrs = expected_aug_attrs + ["CxEperD"]
        expected_aug_insts = insts
        (aug_data, aug_attrs, aug_insts) = (
            augment_with_products._augment_with_combinations(
                aug_data, aug_attrs, aug_insts, ["CxE"], ["D"], 
                fxn=lambda x,y: x/y, fxn_symb='per'))
        self.assertTrue(np.all(aug_data == expected_aug_data))
        self.assertEqual(expected_aug_attrs, aug_attrs)
        self.assertEqual(expected_aug_insts, aug_insts)

if __name__ == '__main__':
    unittest.main()