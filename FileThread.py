#!/usr/bin/env python3


import soundfile as sf
class FileWriting:
    def file_writing_thread(*, q, **soundfile_args):
        """Write data from queue to file until *None* is received."""
        # NB: If you want fine-grained control about the buffering of the file, you
        #     can use Python's open() function (with the "buffering" argument) and
        #     pass the resulting file object to sf.SoundFile().
        with sf.SoundFile(**soundfile_args) as f:
            while True:
                data = q.get()
                if data is None:
                    break
                f.write(data)