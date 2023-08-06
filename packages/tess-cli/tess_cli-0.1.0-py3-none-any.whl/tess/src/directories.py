class Directory:
    SOLUTIONS = 'solutions'
    CASES = 'cases'
    BUILD = 'build'
    TESS = '.tess'
    DEBUG_SOLUTIONS = '.tess/debug/src'
    DEBUG_BUILD = '.tess/debug/build'

    @staticmethod
    def init():
        return [Directory.SOLUTIONS, Directory.CASES, Directory.BUILD,
                Directory.DEBUG_SOLUTIONS, Directory.DEBUG_BUILD]
