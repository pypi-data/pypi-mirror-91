from .pytrace import start
import time

def foo():
    for i in range(3):
        bar()
    bazz()
    import vaex
    df = vaex.open('/data/taxi/yellow_taxi_2009_2015_zones.hdf5')
    start()
    # import viztracer
    def do():
        return df.sum(df.passenger_count)
    # with viztracer.VizTracer(output_file="vaex-profiling.json"):
    for i in range(10):
        t0 = time.time()
        print(do())
        print(time.time() - t0)


def bar():
    bazz()


def bazz():
    pass


def main():
    input("wait...")
    foo()


main()
