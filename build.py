# Darwin all OK
# Windows fails shared builds
# Linux all OK
from conan.packager import ConanMultiPackager
import platform

if __name__ == '__main__':
    builder = ConanMultiPackager(args="--build missing")
    builder.add_common_builds(shared_option_name='libwebp:shared', pure_c=True)
    filtered_builds = []
    for settings, options, env_vars, build_requires in builder.builds:
        if (platform.system() == 'Windows' and options['libwebp:shared'] == False or
                platform.system() == 'Linux' or
                platform.system() == 'Darwin'
            ):
            filtered_builds.append([settings, options, env_vars, build_requires])
    builder.builds = filtered_builds
    builder.run()
