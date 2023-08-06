

Version: 0.2.0

DockerBuild is a 'dockerfile' file generation tools. It converts a file hierarchy tree into a dockerfile.

Files types:

    - Sources: Source files to be downlaoded.
    - (*)Dockerfile.sh: shell script that will be executed in a docker build step.
    - (*)ImageExport: Source file that will be included only in the build process.
    - (*)BuildExport: Source file that will be included to the docker container execution and build process. All @{*} variables will be replaced with the variable value.
    - (*)Entrypoint.sh: Entrypoint shell script.
    - (*)DockerfileAppend: Append dockerfile raw layers.




