# How the semantic python release works

---

#### *python semantic terms*

1. A release refers to the automated process of
    - Determining the next version number
    - Creating a changelog
    - Tagging the release i.e. adding a tag to the latest commit
    - Miscellaneous:
        - publishing the package to pypi
        - Building the package
2. A pre-release refers to a version that is not yet stable and is intended for testing or development purposes.
    - It is indicated by appending a hyphen and a string to the version number, such as `1.0.0-alpha` or `1.0.0-beta`.
    - Does the same as a release, but the version number will be suffixed with a pre-release token
3. Version and Tags
    - The version number reflects the logical progression of your software based on the types of changes introduced.
    - The tag is the actual marker in your Git repository that corresponds to a specific released version. The tag name
      is often the version number prefixed with v.
        - The tag format is specified in the config file, with `tag_format` variable.
    - **Note**: if the tag format changes at some point in the repository’s history, historic versions that no longer
      match this pattern will not be considered as versions.

---

## Version bump

- The semantic release is a tool that automates the versioning and package publishing process based on the *commit*
  *messages* ONLY (Not Branch Name).
- It uses the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification to determine the type
  of version bump (major, minor, patch) and generates a changelog based on the commit history.
- Represents the version number in the SemVer format: `MAJOR.MINOR.PATCH`
- It checks for 3 things in the commits messages
    - fix: increase the patch version by 1 no matter how many fix commits are there before a release
    - feat: increase the minor version by 1 no matter how many feat commits are there before a release
        - if feat and fix are there in the same release, then ```feat``` will be considered first
    - breaking change: increase the major version by 1 no matter how many breaking changes are there before a release
        - if breaking change and feat are there in the same release, then ```breaking change``` will be considered first

Example:

1) If the last release is not present, and the commits are:
    - feat: add new feature
    - fix: fix a bug
      **Output**: the first release will be ```0.1.0```

2) If the last release is 0.1.0, and the commits are:
    - fix: fixed a feature
    - fix: fix a bug
      **Output**: the next release will be ```0.1.1```

3) If the last release is 0.1.0, and the commits are:
    - feat!: new major feature
    - fix: fix a bug
      **Output**: the next release will be ```1.0.0```

- **Note**: The increment can be controlled by using 2 flags in the config file, which are ```major_on_zero```and
  ```allow_zero_version```.
    - allow_zero_version: if ```true```, then first release will be ```0.1.0```. Else it will start from ```1.0.0```
    - major_on_zero: If true, the breaking change will increment the major version by 1, else it will increment the
      minor
      version by 1.
        - when a stable release is happening, then change this from ```false``` to ```true```, so that the next release
          will
          be a major release.
        - This is ignored if allow_zero_version if ```false```, because the first release will be a major release.

## Multibranch release

- Multiple branches can be elected for release
- *Things to follow*:
    - Don't use the same pre-release token for release branches
      ```( A “prerelease token” is the string used to suffix onto the 3-digit form of a full semantic version. For example, in the version 1.2.3-beta.1, the prerelease token is "beta")```
- Use `--prerelease` on:
    - Any **non-main** branch (e.g., `feature/*`, `beta`, `preview`)
    - Preview builds, testing environments, or CI-generated versions
    - Cases where the code isn't ready for production

Example:

1) If all feature branches are given the same pre-release token, then
    - If branches are created after one is merged (sequentially)
        - Version Bump Logic:
            - `feature-1` → `v1.2.0-alpha.1`
            - Merge `feature-1` to `main` → `v1.2.0`
            - `feature-2` → `v1.3.0-alpha.1`
            - `feature-2` merged to `main` → `v1.3.0`
    - If branches are created in parallel
        - Version Bump Logic:
            - `feature-1` → `v1.2.0-alpha.1`
            - `feature-2` → `v1.2.0-alpha.1` → Tag conflict (since the first one is already created)

**Solution**: Use build metadata to differentiate between the two branches

```bash
semantic-release version --build-metadata $(git branch --show-current)
```

- This will create the following versions:
    - `v1.2.0-alpha.1+feature-1`
    - `v1.2.0-alpha.1+feature-2`
- When the branches are merged, it won't cause any conflicts and the bump in the main branch (since it only depends on
  the commit messages) will be:
    - 1st merge → `v1.2.0` (Assuming it has `feat:` commits, can also contain `fix:`)
    - 2nd merge
        - → `v1.3.0` (Assuming it has `feat:` commits, can also contain `fix:`)
        - → `v1.2.1` (Assuming it has `fix:` commits only)

- When the pre-release token is not used for ```feature``` or ```testing``` branches
    - A feature branch can have a full tagged release (e.g., `v1.2.0`) even if it is not ready for production.
        - This can cause tag conflicts when the version bump is being done in ```main``` branch, since the same tag is
          already created in the feature branch.
        - Which leads to a premature or unintended release.

### Multibranch Release Configuration

You can define **release groups** in your configuration file (e.g., `pyproject.toml`) to control how different branches
produce releases.

- Parameters:
    - **`match`**
        - **Required:** Yes
        - **Default:** N/A
        - **Description:** Python regex to match the active branch name. If it matches, this release group is applied.
    - **`prerelease`**
        - **Required:** No
        - **Default:** `false`
        - **Description:** If set to `true`, branches in this group generate prereleases instead of full releases.
    - **`prerelease_token`**
        - **Required:** No
        - **Default:** `"rc"`
        - **Description:** The token used in the version string for prereleases (e.g., `v1.2.0-alpha.1` if token is
          `"alpha"`).

Example:

```toml
[tool.semantic_release.branches.features]
match = "^feature-.*"
prerelease = true
prerelease_token = "alpha"
```

- All `feature-*` branches produce prereleases like `v1.2.0-alpha.1`.

## Changelog

- Dependent variables:
    - `mode` and `insertion_flag`
        - mode → `init` and `update` (init will create a new changelog everytime)
        - `insertion_flag` is used with `update` mode to insert the new changes at the top or bottom of the changelog
          file.
- `exclude_commit_patterns` → This can be used to remove commits that could not be parsed by the parser and are placed
  in the unknown section in the release or changelog.
- The difference between the changelog and release notes is that the release notes only contain the changes for the
  current release

## Other configurations

- `commit_author` → The author who will increment the version and commit the changes
- `commit_message` → The message that will be used for the commit when doing a release

## Commit Parser

- It is the commit parser’s job to extract the change impact from the commit message to determine the severity of the
  changes and then subsequently determine the semver level that the version should be bumped to for the next release.

1) Parsers →
    - Both Conventional and Angular Parser have same
        - version bump determination
        - changelog generation
        - pull request identification
        - Linked issues identification
        - squash merge commit evaluation
    - All of PSR built-in parsers implement common pull/merge request identifier detection logic to extract
      pull/merge request numbers from the commit message

2) Parser options →
    - The conventional parse options are derived from the Angular parser options