import datetime
import subprocess

def get_commit_messages(previous_version):
    cmd = ['git', 'log', f'{previous_version}..HEAD', '--pretty=format:%s']
    commit_messages = subprocess.check_output(cmd).decode().splitlines()
    return commit_messages

def generate_changelog():
    # Retrieve the previous version from the README file or a separate changelog file
    # Replace this with your actual logic to fetch the previous version
    previous_version = '1.0.0'

    current_version = '1.1.0'
    commit_messages = get_commit_messages(previous_version)

    changelog = f"### Version {current_version} ({datetime.date.today()})\n\n"
    changelog += "\n".join(f"- {message}" for message in commit_messages)

    # Read the existing README file
    with open('README.md', 'r') as readme_file:
        readme_content = readme_file.read()

    # Append the changelog at the bottom of the README file
    readme_content += f"\n{changelog}"

    # Write the updated README file
    with open('README.md', 'w') as readme_file:
        readme_file.write(readme_content)

    print("Changelog generated successfully.")

if __name__ == '__main__':
    generate_changelog()
