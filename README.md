# How the semantic python release works

---

#### *python semantic terms*

1. A release refers to the automated process of
    - Determining the next version number
    - Creating a changelog
    - Tagging the release i.e adding a tag to the latest commit
    - Miscellaneous:
        - publishing the package to pypi
        - Building the package
2. A pre-release refers to a version that is not yet stable and is intended for testing or development purposes.
    - It is indicated by appending a hyphen and a string to the version number, such as `1.0.0-alpha` or `1.0.0-beta`.
    - Does the same as a release, but the version number will be suffixed with a pre-release token

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

```commandline
semantic-release version --build-metadata $(git branch --show-current)
```

- This will create the following versions:
    - `v1.2.0-alpha.1+feature-1`
    - `v1.2.0-alpha.1+feature-2`
- When the branches are merged, it won't cause any conflicts and the bump in the main branch (since it only depends on
  the)
  commit messages) will be:
    - 1st merge → `v1.2.0` (Assuming it has `feat:` commits, can also contain `fix:`)
    - 2nd merge
        - → `v1.3.0` (Assuming it has `feat:` commits, can also contain `fix:`)
        - → `v1.2.1` (Assuming it has `fix:` commits only)

## Changelog