import pathlib
from pdf_extract import extract

SAMPLE = pathlib.Path(__file__).parent.resolve() / 'sample.pdf'

def test_basic_load():
    path = str(SAMPLE)
    pages_out, chars_out, objs_out, fonts_out = extract(path)

    assert len(chars_out.arrays['char']) == 2913
    assert len(objs_out.arrays['txt_obj_id']) == 36
    assert len(fonts_out.arrays['font_obj_id']) == 3
    assert len(pages_out.arrays['page']) == 1

def test_pyarrow_tables():
    path = str(SAMPLE)
    pages_out, chars_out, objs_out, fonts_out = extract(path)

    assert len(chars_out.table) == 2913
    assert len(objs_out.table) == 36
    assert len(fonts_out.table) == 3
    assert len(pages_out.table) == 1

def test_string_extraction():
    path = str(SAMPLE)
    _, chars_out, _, _ = extract(path)

    TEST_STRING = (
        'Sample PDF\r\n'
        'This is a simple PDF file. Fun fun fun.\r\n'
        'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Phasellus facilisis odio sed mi. \r\n'
        'Curabitur suscipit. Nullam vel nisi. Etiam semper ipsum ut lectus. Proin aliquam, erat eget \r\n'
        'pharetra commodo, eros mi condimentum quam, sed commodo justo quam ut velit. \r\n'
        'Integer a erat. Cras laoreet ligula cursus enim. Aenean scelerisque velit et tellus. \r\n'
        'Vestibulum dictum aliquet sem. Nulla facilisi. Vestibulum accumsan ante vitae elit. Nulla \r\n'
        'erat dolor, blandit in, rutrum quis, semper pulvinar, enim. Nullam varius congue risus. \r\n'
        'Vivamus sollicitudin, metus ut interdum eleifend, nisi tellus pellentesque elit, tristique \r\n'
        'accumsan eros quam et risus. Suspendisse libero odio, mattis sit amet, aliquet eget, \r\n'
        'hendrerit vel, nulla. Sed vitae augue. Aliquam erat volutpat. Aliquam feugiat vulputate nisl. \r\n'
        'Suspendisse quis nulla pretium ante pretium mollis. Proin velit ligula, sagittis at, egestas a, \r\n'
        'pulvinar quis, nisl.\r\n'
        
        'Pellentesque sit amet lectus. Praesent pulvinar, nunc quis iaculis sagittis, justo quam \r\n'
        'lobortis tortor, sed vestibulum dui metus venenatis est. Nunc cursus ligula. Nulla facilisi. \r\n'
        'Phasellus ullamcorper consectetuer ante. Duis tincidunt, urna id condimentum luctus, nibh \r\n'
        'ante vulputate sapien, id sagittis massa orci ut enim. Pellentesque vestibulum convallis \r\n'
        'sem. Nulla consequat quam ut nisl. Nullam est. Curabitur tincidunt dapibus lorem. Proin \r\n'
        'velit turpis, scelerisque sit amet, iaculis nec, rhoncus ac, ipsum. Phasellus lorem arcu, \r\n'
        'feugiat eu, gravida eu, consequat molestie, ipsum. Nullam vel est ut ipsum volutpat \r\n'
        'feugiat. Aenean pellentesque.\r\n'
        
        'In mauris. Pellentesque dui nisi, iaculis eu, rhoncus in, venenatis ac, ante. Ut odio justo, \r\n'
        'scelerisque vel, facilisis non, commodo a, pede. Cras nec massa sit amet tortor volutpat \r\n'
        'varius. Donec lacinia, neque a luctus aliquet, pede massa imperdiet ante, at varius lorem \r\n'
        'pede sed sapien. Fusce erat nibh, aliquet in, eleifend eget, commodo eget, erat. Fusce \r\n'
        'consectetuer. Cras risus tortor, porttitor nec, tristique sed, convallis semper, eros. Fusce \r\n'
        'vulputate ipsum a mauris. Phasellus mollis. Curabitur sed urna. Aliquam nec sapien non \r\n'
        'nibh pulvinar convallis. Vivamus facilisis augue quis quam. Proin cursus aliquet metus. \r\n'
        'Suspendisse lacinia. Nulla at tellus ac turpis eleifend scelerisque. Maecenas a pede vitae \r\n'
        'enim commodo interdum. Donec odio. Sed sollicitudin dui vitae justo.\r\n'
        'Morbi elit nunc, facilisis a, mollis a, molestie at, lectus. Suspendisse eget mauris eu tellus \r\n'
        'molestie cursus. Duis ut magna at justo dignissim condimentum. Cum sociis natoque \r\n'
        'penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vivamus varius. Ut sit \r\n'
        'amet diam suscipit mauris ornare aliquam. Sed varius. Duis arcu. Etiam tristique massa \r\n'
        'eget dui. Phasellus congue. Aenean est erat, tincidunt eget, venenatis quis, commodo at, \r\n'
        'quam.'
    )

    assert TEST_STRING == ''.join(chars_out.table['char'].to_pylist())