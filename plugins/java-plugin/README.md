# Java Plugin

Java code analysis and execution plugin for the Claude multi-plugin agent.

## Features

- **Code Analysis**: Parse and analyze Java code structure
- **AST Analysis**: Deep analysis of Abstract Syntax Trees
- **Dependency Analysis**: Track imports and dependencies
- **Code Search**: Search through Java codebases
- **Code Execution**: Compile and execute Java code
- **Testing**: Run and analyze test suites
- **Linting**: Code quality checks

## Build

```bash
mvn clean install
```

## Run

```bash
mvn exec:java -Dexec.mainClass="com.claude.plugin.java.Main"
```

## Test

```bash
mvn test
```

## Requirements

- Java 17 or higher
- Maven 3.6+
