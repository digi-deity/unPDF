import numpy as np
import pyarrow as pa

class PageTable:
    def __init__(self, n):
        self.arrays = {
            'page': np.arange(n, dtype=np.intc),
            'width': np.ndarray((n,), dtype=np.single),
            'height': np.ndarray((n,), dtype=np.single),
            'left': np.ndarray((n,), dtype=np.single),
            'right': np.ndarray((n,), dtype=np.single),
            'bottom': np.ndarray((n,), dtype=np.single),
            'top': np.ndarray((n,), dtype=np.single),
        }

        self.table = pa.Table.from_pydict({k: pa.array(v) for k, v in self.arrays.items()})

class FontTable:
    def __init__(self, uq_fontptr: np.ndarray):
        n = len(uq_fontptr)

        self.arrays = {
            'font_obj_id': uq_fontptr,
            'flags': np.ndarray((n,), dtype=np.intc),
            'weight': np.ndarray((n,), dtype=np.intc),
            'italic_angle': np.ndarray((n,), dtype=np.intc),
            'base_fontname': np.ndarray((n,), dtype=object),
            'family_fontname': np.ndarray((n,), dtype=object),
        }

    @property
    def table(self):
        return pa.Table.from_pydict({k: pa.array(v) for k, v in self.arrays.items()})

class TextObjTable:
    def __init__(self, uq_objptr: np.ndarray):
        n = len(uq_objptr)

        self.arrays = {
            'txt_obj_id': uq_objptr,
            'fontsize': np.ndarray((n,), dtype=np.single),
            'has_transparency': np.ndarray((n,), dtype=np.intc),
            'font_obj_id': np.ndarray((n,), dtype=np.uint64),
            'color_R': np.ndarray((n,), dtype=np.uintc),
            'color_G': np.ndarray((n,), dtype=np.uintc),
            'color_B': np.ndarray((n,), dtype=np.uintc),
            'color_A': np.ndarray((n,), dtype=np.uintc),
            'tmatrix_a': np.ndarray((n,), dtype=np.single),
            'tmatrix_b': np.ndarray((n,), dtype=np.single),
            'tmatrix_c': np.ndarray((n,), dtype=np.single),
            'tmatrix_d': np.ndarray((n,), dtype=np.single),
            'tmatrix_e': np.ndarray((n,), dtype=np.single),
            'tmatrix_f': np.ndarray((n,), dtype=np.single),
        }

        self.table = pa.Table.from_pydict({k: pa.array(v) for k, v in self.arrays.items()})
class CharTable:

    def __init__(self, n):
        self.arrays = {
            'page': np.ndarray((n,), dtype=np.intc),
            'char': np.ndarray((n,), dtype=np.uintc),
            'is_generated': np.ndarray((n,), dtype=np.intc),
            'txt_obj_id': np.ndarray((n,), dtype=np.uint64),
            'left': np.ndarray((n,), dtype=np.double),
            'right': np.ndarray((n,), dtype=np.double),
            'bottom': np.ndarray((n,), dtype=np.double),
            'top': np.ndarray((n,), dtype=np.double),
            'loose_left': np.ndarray((n,), dtype=np.single),
            'loose_right': np.ndarray((n,), dtype=np.single),
            'loose_bottom': np.ndarray((n,), dtype=np.single),
            'loose_top': np.ndarray((n,), dtype=np.single),
            'bbox_ok': np.ndarray((n,), dtype=np.intc),
            'loose_bbox_ok': np.ndarray((n,), dtype=np.intc),
            'hyphen': np.ndarray((n,), dtype=np.intc),
            'has_unicode_map_error': np.ndarray((n,), dtype=np.intc),
        }

    @property
    def table(self):
        arrays = self.arrays.copy()
        arrays['char'] = arrays['char'].tobytes().decode('utf32')

        return pa.Table.from_pydict({k: pa.array(v) for k, v in arrays.items()})