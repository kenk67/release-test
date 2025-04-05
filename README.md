# How the semantic python release works

## Version bump

- The semantic release is a tool that automates the versioning and package publishing process based on the commit
  messages.
- It uses the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification to determine the type
  of version bump (major, minor, patch) and generates a changelog based on the commit history.
- Represents the version number in the format of `MAJOR.MINOR.PATCH`
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

## Changelog