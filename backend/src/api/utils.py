import os
import shutil


def flatten_dir(dir_):
    for cur_dir, _, files in os.walk(dir_):
        if cur_dir == dir_:
            continue

        [shutil.move(os.path.join(cur_dir, f), os.path.join(dir_, f)) for f in files]

    [shutil.rmtree(path) for d in os.listdir(dir_) if os.path.isdir(path := os.path.join(dir_, d))]
