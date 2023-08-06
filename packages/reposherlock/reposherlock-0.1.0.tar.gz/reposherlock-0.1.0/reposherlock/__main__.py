import argparse
import json
import logging
from github import GitHub
from os.path import abspath, join
from sys import exit

if __name__ == '__main__':
    # Collect relevant parameters from user
    parser = argparse.ArgumentParser(description="Pull data from software repositories.")
    parser.add_argument('--user', metavar='u', type=str, required=True,
                        help='Your username.')
    parser.add_argument('--token', metavar='t', type=str, required=True,
                        help='The token provided to you by your repository service.')
    parser.add_argument('--target', metavar='r', type=str, required=True,
                        help='The repository whose data you want to pull.')
    parser.add_argument('--type', metavar='s', type=str, required=True,
                        help="Your repository management service [GitHub|BitBucket].")
    parser.add_argument('--outdir', metavar='d', type=str, required=True,
                        help="The output directory to save the queried data.")
    parser.add_argument('--pages', metavar='p', type=int, required=False, default=1000,
                        help='How many pages of data to fetch. Default is 1000.')

    # Set up logging
    logger = logging.getLogger('reposherlock')
    logging.basicConfig(level=logging.INFO)
    logger.info('Logger calibrated.')

    args = vars(parser.parse_args())

    # Check for parameter validity
    if args['user'] is None:
        logger.fatal("No username provided. Aborting...")
        exit(1)
    if args['token'] is None:
        logger.fatal("No token provided. Aborting...")
        exit(1)
    if args['target'] is None:
        logger.fatal("No target repository provided. Aborting...")
        exit(1)
    if args['type'] is None:
        logger.fatal("Repository service not specified. Aborting...")
        exit(1)
    if args['outdir'] is None:
        logger.fatal("No output directory provided. Aborting...")
        exit(1)

    # Set up output directory
    output_directory = abspath(args['outdir'])
    repository_file_prefix = args['target'].replace('/', '_')
    repository_issues_filename = repository_file_prefix + '_issues.json'
    repository_pull_requests_filename = repository_file_prefix + '_prs.json'
    repository_commits_filename = repository_file_prefix + '_commits.json'
    output_issues = join(output_directory, repository_issues_filename)
    output_pull_requests = join(output_directory, repository_pull_requests_filename)
    output_commits = join(output_directory, repository_commits_filename)

    # Output everything back to the user for clarity
    print('Pulling data with the following specifications:')
    print("> Repository hosted at: %s" % args['type'])
    print("> Username: %s" % args['user'])
    print("> Token: %s" % args['token'])
    print("> Target Repository: %s" % args['target'])
    print("> Output Directory: %s" % output_directory)
    print("> Pages to retrieve: %d" % args['pages'])

    # Create client based on choice given
    if args['type'].lower() == 'github':
        client = GitHub(args['user'], args['token'])
    else:
        logger.fatal('Unknown service provided. Aborting...')
        exit(1)

    # Pull data
    print("Retrieving issues for %s" % args['target'])
    issues = client.get_issues(args['target'], args['pages'])
    print("Retrieving pull/merge requests for %s" % args['target'])
    pull_requests = client.get_pull_requests(args['target'], args['pages'])
    print("Retrieving commits for %s" % args['target'])
    commits = client.get_commits(args['target'], args['pages'])

    # Write output to file
    with open(output_issues, 'w') as issues_out:
        json.dump(issues, issues_out)
    with open(output_pull_requests, 'w') as pull_requests_out:
        json.dump(pull_requests, pull_requests_out)
    with open(output_commits, 'w') as commits_out:
        json.dump(commits, commits_out)
    print("Issues written to: %s" % output_issues)
    print("Pull/Merge requests written to: %s" % output_pull_requests)
    print("Commits written to: %s" % output_commits)
