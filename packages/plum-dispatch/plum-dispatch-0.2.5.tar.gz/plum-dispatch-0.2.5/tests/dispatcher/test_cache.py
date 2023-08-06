from plum import Dispatcher, List, clear_all_cache, Referentiable, Self
from plum.type import subclasscheck_cache
from ..util import benchmark


def test_cache_function_call_performance_and_correctness():
    # Test performance.
    dispatch = Dispatcher()

    def f_native(x):
        pass

    @dispatch(object)
    def f(x):
        pass

    @dispatch({int, float})
    def f(x):
        pass

    @dispatch({int, float, str})
    def f(x):
        pass

    dur_native = benchmark(f_native, (1,))
    dur_plum_first = benchmark(f, (1,), n=1)
    dur_plum = benchmark(f, (1,))

    # A cached call should not be more than 15 times slower than a native
    # call.
    assert dur_plum <= 15 * dur_native, "compare native"

    # A first call should not be more than 1000 times slower than a cached call.
    assert dur_plum_first <= 1000 * dur_plum, "compare first"

    # The cached call should be at least 20 times faster than a first call.
    assert dur_plum <= dur_plum_first / 20, "cache performance"

    # Test cache correctness.
    assert f(1) is None, "cache correctness 1"

    @dispatch(int)
    def f(x):
        return 1

    assert f(1) == 1, "cache correctness 2"


def test_cache_class_call_performance():
    class ANative:
        def __call__(self, x):
            pass

        def go(self, x):
            pass

        def go_again(self, x):
            pass

    class A(metaclass=Referentiable):
        _dispatch = Dispatcher(in_class=Self)

        @_dispatch(int)
        def __call__(self, x):
            pass

        @_dispatch(str)
        def __call__(self, x):
            pass

        @_dispatch(int)
        def go(self, x):
            pass

        @_dispatch(str)
        def go(self, x):
            pass

        @_dispatch(int)
        def go_again(self, x):
            pass

        @_dispatch(str)
        def go_again(self, x):
            pass

    a_native = ANative()
    a = A()

    # Test performance of calls. See above previous test.
    dur_native = benchmark(a_native, (1,))
    dur_plum_first = benchmark(a, (1,), n=1)
    dur_plum = benchmark(a, (1,))
    assert dur_plum <= 25 * dur_native, "compare native call"
    assert dur_plum_first <= 1000 * dur_plum, "compare first call"
    assert dur_plum <= dur_plum_first / 10, "cache performance call"

    # Test performance of method calls.
    dur_native = benchmark(lambda x: a_native.go(x), (1,))
    dur_plum_first = benchmark(lambda x: a.go(x), (1,), n=1)
    dur_plum = benchmark(lambda x: a.go(x), (1,))
    assert dur_plum <= 25 * dur_native, "compare native method"
    assert dur_plum_first <= 1000 * dur_plum, "compare first method"
    assert dur_plum <= dur_plum_first / 10, "cache performance method"

    # Test performance of static calls.
    dur_native = benchmark(lambda x: ANative.go_again(a_native, x), (1,))
    dur_plum_first = benchmark(lambda x: A.go_again(a, x), (1,), n=1)
    dur_plum = benchmark(lambda x: A.go_again(a, x), (1,))
    assert dur_plum <= 25 * dur_native, "compare native static"
    assert dur_plum_first <= 1000 * dur_plum, "compare first static"
    assert dur_plum <= dur_plum_first / 10, "cache performance static"


def test_cache_clearing():
    dispatch = Dispatcher()

    @dispatch(object)
    def f(x):
        return 1

    @dispatch(List(int))
    def f(x):
        return 1

    f(1)

    # Check that cache is used.
    assert len(f.methods) == 2
    assert len(f.precedences) == 2
    assert f._parametric

    dispatch.clear_cache()

    # Check that cache is cleared.
    assert len(f.methods) == 0
    assert len(f.precedences) == 0
    assert not f._parametric

    f(1)
    clear_all_cache()

    # Again check that cache is cleared.
    assert len(f.methods) == 0
    assert len(f.precedences) == 0
    assert len(subclasscheck_cache) == 0
    assert not f._parametric
