import argparse
import os
import re
from sys import stderr

import yaml
from pkg_resources import get_distribution, DistributionNotFound

regex_version_pattern = re.compile(r"((?:__)?version(?:__)? ?= ?[\"'])(.+?)([\"'])")


def is_valid_helm_chart(content):
    """
    Check if input dictionary contains mandatory keys of a Helm Chart.yaml file,
    as documented here https://helm.sh/docs/topics/charts/#the-chartyaml-file
    :param content: parsed YAML file as dictionary of key values
    :return: True if dict contains mandatory values, else False
    """
    return all(x in content for x in ['apiVersion', 'name', 'version'])


def get_setup_py_version(content):
    """
    Extract 'version' value using regex from 'content'
    :param content: the content of a setup.py file
    :return: version value as string
    """
    version_match = regex_version_pattern.findall(content)
    if len(version_match) > 1:
        raise RuntimeError("More than one 'version' found: {0}".format(version_match))
    if not version_match:
        raise RuntimeError("Unable to find version string in: {0}".format(content))
    return version_match[0][1]


def set_setup_py_version(version, content):
    """
    Replace version in setup.py file using regex,
    g<1> contains the string left of version
    g<3> contains the string right of version
    :param version: string
    :param content: content of setup.py as string
    :return: content of setup.py file with 'version'
    """
    return regex_version_pattern.sub(r'\g<1>{}\g<3>'.format(version), content)


def is_semantic_string(semantic_string):
    """
    Check if input string is a semantic version as defined here: https://github.com/semver/semver/blob/master/semver.md,
    The version is allowed a lower case 'v' character.
    Function will search a match according to the regular expresion, so for example '1.1.2-prerelease+meta' is valid,
    then make sure there is and exact singe match and validate if each of x,y,z is an integer.
    return {'prefix': boolean, 'version': [x, y, z], 'release': 'some-release', 'metadata': 'some-metadata'} if True

    :param semantic_string: string
    :return: dict if True, else False
    """
    if type(semantic_string) != str or len(semantic_string) == 0:
        return False

    version_prefix = False
    # In case the version if of type 'v2.2.5' then save 'v' prefix and cut it for further 'semver' validation
    if semantic_string[0] == 'v':
        semantic_string = semantic_string[1:]
        version_prefix = True

    semver_regex = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"  # Match x.y.z
                              # Match -sometext-12.here
                              r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
                              r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
                              # Match +more.123.here
                              r"(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$")
    # returns a list of tuples, for example [('2', '2', '7', 'alpha', '')]
    match = semver_regex.findall(semantic_string)

    # There was no match using 'semver_regex', since if 0 or more then single match found and empty list returned
    if len(match) == 0:
        return False

    try:
        semantic_array = [int(n) for n in match[0][:3]]
    except ValueError:
        return False

    return {'prefix': version_prefix, 'version': semantic_array, 'release': match[0][3], 'metadata': match[0][4]}


def bump_version(version_array, level):
    """
    Perform ++1 action on the array [x, y, z] cell,
    Input values are assumed to be validated
    :param version_array: int array of [x, y, z] validated array
    :param level: string represents major|minor|patch
    :return: int array with new value
    """
    if type(version_array) != list:
        raise ValueError("Error, invalid version_array: '{}', "
                         "should be [x, y, z].".format(version_array))

    if level == 'major':
        version_array[0] += 1
        version_array[1] = 0
        version_array[2] = 0
    elif level == 'minor':
        version_array[1] += 1
        version_array[2] = 0
    elif level == 'patch':
        version_array[2] += 1
    else:
        raise ValueError("Error, invalid level: '{}', "
                         "should be major|minor|patch.".format(level))

    return version_array


def get_self_version(dist_name):
    """
    Return version number of input distribution name,
    If distribution not found return not found indication
    :param dist_name: string
    :return: version as string
    """
    try:
        return get_distribution(dist_name).version
    except DistributionNotFound:
        return 'version not found'


def assemble_version_string(prefix, version_array, release, metadata):
    """
    reconstruct version
    :param prefix: boolean
    :param version_array: list of ints
    :param release: string
    :param metadata: sting
    :return: string
    """
    result_string = ''
    if prefix:
        result_string = 'v'
    result_string += '.'.join(str(x) for x in version_array)
    if release:
        result_string += '-' + release

    if metadata:
        result_string += '+' + metadata

    return result_string


def write_version_to_file(file_path, file_content, version, app_version):
    """
    Write the 'version' or 'appVersion' to a given file
    :param file_path: full path to file as string
    :param file_content: content of the file as string
    :param version: version to set as string
    :param app_version: boolean, if True then set the appVersion key
    """
    # Append the 'new_version' to relevant file
    with open(file_path, 'w') as outfile:
        filename, file_extension = os.path.splitext(file_path)
        if file_extension == '.py':
            outfile.write(set_setup_py_version(version, file_content))
        elif file_extension == '.yaml' or file_extension == '.yml':
            if app_version:
                file_content['appVersion'] = version
            else:
                file_content['version'] = version
            yaml.dump(file_content, outfile, default_flow_style=False)
        elif os.path.basename(filename) == 'VERSION':
            outfile.write(version)
        outfile.close()


def read_version_from_file(file_path, app_version):
    """
    Read the 'version' or 'appVersion' from a given file
    :param file_path: full path to file as string
    :param app_version: boolean, if True return appVersion from Helm chart
    :return: dict containing file content and version as {'file_content': file_content, 'version': current_version}
    """
    with open(file_path, 'r') as stream:
        filename, file_extension = os.path.splitext(file_path)

        if file_extension == '.py':  # Case setup.py files
            file_content = stream.read()
            current_version = get_setup_py_version(file_content)
        elif file_extension == '.yaml' or file_extension == '.yml':  # Case Helm chart files
            try:
                file_content = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
            # Make sure Helm chart is valid and contains minimal mandatory keys
            if is_valid_helm_chart(file_content):
                if app_version:
                    current_version = file_content.get('appVersion', None)

                    # user passed the 'app-version' flag, but helm chart file does not contain the 'appVersion' field
                    if not current_version:
                        raise ValueError(
                            "Could not find 'appVersion' field in helm chart.yaml file: {}".format(file_content)
                        )
                else:
                    current_version = file_content['version']
            else:
                raise ValueError("Input file is not a valid Helm chart.yaml: {0}".format(file_content))
        else:  # Case file name is just 'VERSION'
            if os.path.basename(filename) == 'VERSION':
                # A version file should ONLY contain a valid semantic version string
                file_content = None
                current_version = stream.read()
            else:
                raise ValueError("File name or extension not known to this app: {}{}"
                                 .format(os.path.basename(filename), file_extension))

    return {'file_content': file_content, 'version': current_version}


def print_invalid_version(version):
    print("Invalid semantic version format: {}\n"
          "Make sure to comply with https://semver.org/ (lower case 'v' prefix is allowed)".format(version),
          file=stderr)


def main():
    parser = argparse.ArgumentParser(description='Python version bumper')
    subparsers = parser.add_subparsers(dest='sub_command')

    parser.add_argument('--version', action='version',
                        version='%(prog)s {}'.format(get_self_version('pybump')),
                        help='Print version and exit')
    parser.add_argument('--verify', required=False,
                        help='Verify if input string is a valid semantic version')

    # Define parses that is shared, and will be used as 'parent' parser to all others
    base_sub_parser = argparse.ArgumentParser(add_help=False)
    base_sub_parser.add_argument('--file', help='Path to Chart.yaml/setup.py/VERSION file', required=True)
    base_sub_parser.add_argument('--app-version', action='store_true',
                                 help='Bump Helm chart appVersion, relevant only for Chart.yaml files', required=False)

    # Sub-parser for bump version command
    parser_bump = subparsers.add_parser('bump', parents=[base_sub_parser])
    parser_bump.add_argument('--level', choices=['major', 'minor', 'patch'], help='major|minor|patch', required=True)
    parser_bump.add_argument('--quiet', action='store_true', help='Do not print new version', required=False)

    # Sub-parser for set version command
    parser_set = subparsers.add_parser('set', parents=[base_sub_parser])

    # Set mutual exclusion https://docs.python.org/3/library/argparse.html#mutual-exclusion,
    # To make sure that at least one of the mutually exclusive arguments is required
    set_group = parser_set.add_mutually_exclusive_group(required=True)
    set_group.add_argument('--auto', action='store_true',
                           help='Set automatic release / metadata from current git branch for current version')
    set_group.add_argument('--set-version',
                           help='Semantic version to set as a combination of \'vX.Y.Z-release+metadata\'')
    parser_set.add_argument('--quiet', action='store_true', help='Do not print new version', required=False)

    # Sub-parser for get version command
    parser_get = subparsers.add_parser('get', parents=[base_sub_parser])
    parser_get.add_argument('--sem-ver', action='store_true', help='Get the main version only', required=False)
    parser_get.add_argument('--release', action='store_true', help='Get the version release only', required=False)
    parser_get.add_argument('--metadata', action='store_true', help='Get the version metadata only', required=False)

    args = vars(parser.parse_args())

    # Case where no args passed, sub_command is mandatory
    if args['sub_command'] is None:
        if args['verify']:
            if is_semantic_string(args['verify']):
                print('{} is valid'.format(args['verify']))
            else:
                print_invalid_version(args['verify'])
                exit(1)
        else:
            parser.print_help()
        exit(0)

    # Read current version from the given file
    file_data = read_version_from_file(args['file'], args['app_version'])
    current_version = file_data.get('version')
    file_content = file_data.get('file_content')

    current_version_dict = is_semantic_string(current_version)
    if not current_version_dict:
        print_invalid_version(current_version)
        exit(1)

    if args['sub_command'] == 'get':
        if args['sem_ver']:
            # Join the array of current_version_dict by dots
            print('.'.join(str(x) for x in current_version_dict.get('version')))
        elif args['release']:
            print(current_version_dict.get('release'))
        elif args['metadata']:
            print(current_version_dict.get('metadata'))
        else:
            print(current_version)
    else:
        # Set new_version to be invalid first
        new_version = ''

        # Set the 'new_version' value
        if args['sub_command'] == 'set':
            # Case set-version argument passed, just set the new version with its value
            if args['set_version']:
                new_version = args['set_version']
            # Case the 'auto' flag was set, set release with current git branch name and metadata with hash
            elif args['auto']:
                from git import Repo, InvalidGitRepositoryError
                # get the directory path of current working file
                file_dirname_path = os.path.dirname(args['file'])
                try:
                    repo = Repo(path=file_dirname_path)
                    new_version = assemble_version_string(prefix=current_version_dict.get('prefix'),
                                                          version_array=current_version_dict.get('version'),
                                                          release=repo.active_branch.name,
                                                          metadata=str(repo.active_branch.commit))
                except InvalidGitRepositoryError:
                    print("{} is not a valid git repo".format(file_dirname_path), file=stderr)
                    exit(1)
            # Should never reach this point due to argparse mutual exclusion, but set safety if statement anyway
            else:
                print("set-version or auto flags are mandatory", file=stderr)
                exit(1)
        else:  # bump version ['sub_command'] == 'bump'
            # Only bump value of the 'version' key
            new_version_array = bump_version(current_version_dict.get('version'), args['level'])
            # Reconstruct new version with rest dict parts if exists
            new_version = assemble_version_string(prefix=current_version_dict.get('prefix'),
                                                  version_array=new_version_array,
                                                  release=current_version_dict.get('release'),
                                                  metadata=current_version_dict.get('metadata'))
        if not is_semantic_string(new_version):
            print_invalid_version(new_version)
            exit(1)
        # Write the new version with relevant content back to the file
        write_version_to_file(args['file'], file_content, new_version, args['app_version'])

        if args['quiet'] is False:
            print(new_version)


if __name__ == "__main__":
    main()
