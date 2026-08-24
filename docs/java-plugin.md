# Java Plugin

The Java plugin provides comprehensive code analysis and execution capabilities for Java code.

## Features

### Code Analysis

- **Java Parser**: Parse Java source code and extract structure
- **AST Analyzer**: Extract methods, fields, and calculate complexity
- **Dependency Analyzer**: Track imports and dependencies across projects

### Code Tools

- **Code Search**: Search for patterns and symbols in Java files
- **Code Reader**: Read files and extract information
- **Code Writer**: Write and modify Java files
- **Test Runner**: Execute JUnit tests
- **Linter**: Check code quality and style

### Code Execution

- **Executor**: Compile and run Java code
- **Sandbox**: Execute code in a restricted security context

## Usage

### Parse Code

```java
Main plugin = new Main();
PluginRequest request = new PluginRequest("parse", 
    "public class Test { void method() {} }");
PluginResponse response = plugin.execute(request);
```

### Analyze Code

```java
PluginRequest request = new PluginRequest("analyze", javaCode);
PluginResponse response = plugin.execute(request);
// Returns: methods, fields, complexity, metrics
```

### Search Code

```java
PluginRequest request = new PluginRequest("search", 
    "{\"query\": \"public.*calculate\", \"path\": \"src/\"}");
PluginResponse response = plugin.execute(request);
```

### Execute Code

```java
PluginRequest request = new PluginRequest("execute", javaCode);
PluginResponse response = plugin.execute(request);
```

## Building

### Compile

```bash
cd plugins/java-plugin
mvn clean compile
```

### Run Tests

```bash
mvn test
```

### Package

```bash
mvn package
```

### Run

```bash
mvn exec:java -Dexec.mainClass="com.claude.plugin.java.Main"
```

## API Reference

See the JavaDoc documentation for detailed API reference:

```bash
mvn javadoc:javadoc
```

## Development

### Code Style

The project follows standard Java coding conventions:

- Class names: PascalCase
- Method names: camelCase
- Constants: UPPER_SNAKE_CASE
- Package names: lowercase

### Dependencies

Main dependencies:

- Java 17+
- JUnit 5 for testing
- Gson for JSON processing

### IDE Setup

Import as a Maven project in your IDE:

- IntelliJ IDEA: File → Open → Select pom.xml
- Eclipse: File → Import → Maven → Existing Maven Projects
- VS Code: Open folder with Java extension pack installed
