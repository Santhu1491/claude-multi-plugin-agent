#!/bin/bash

# Run Java plugin

set -e

echo "Starting Java Plugin..."

cd plugins/java-plugin

# Build if needed
if [ ! -d "target/classes" ]; then
    echo "Building plugin..."
    mvn clean compile
fi

# Run the plugin
mvn exec:java -Dexec.mainClass="com.claude.plugin.java.Main" "$@"
