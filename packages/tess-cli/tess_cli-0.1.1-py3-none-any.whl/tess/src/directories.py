class Directory:
    SOLUTIONS = 'solutions'
    CASES = 'cases'
    BUILD = 'build'
    TESS = '.tess'
    DEBUG_SOLUTIONS = '.tess/debug/src'
    DEBUG_BUILD = '.tess/debug/build'
    CUSTOM_CONFIG_LINUX = '~/.config/tess'
    CUSTOM_CONFIG_MAC = '~/Library/Application\\ Support/Tess'

    @staticmethod
    def init():
        return [Directory.SOLUTIONS, Directory.CASES, Directory.BUILD,
                Directory.DEBUG_SOLUTIONS, Directory.DEBUG_BUILD]
