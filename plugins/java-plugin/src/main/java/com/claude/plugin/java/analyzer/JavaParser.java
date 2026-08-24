package com.claude.plugin.java.analyzer;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;
import java.util.regex.Matcher;

/**
 * Java code parser for extracting code structure.
 */
public class JavaParser {
    
    /**
     * Parse Java source code from a string.
     */
    public ParseResult parse(String code) {
        ParseResult result = new ParseResult();
        
        // Extract package
        result.packageName = extractPackage(code);
        
        // Extract imports
        result.imports = extractImports(code);
        
        // Extract classes
        result.classes = extractClasses(code);
        
        return result;
    }
    
    /**
     * Parse Java source code from a file.
     */
    public ParseResult parseFile(String filePath) throws IOException {
        String code = Files.readString(Path.of(filePath));
        return parse(code);
    }
    
    private String extractPackage(String code) {
        Pattern pattern = Pattern.compile("package\\s+([\\w.]+)\\s*;");
        Matcher matcher = pattern.matcher(code);
        return matcher.find() ? matcher.group(1) : null;
    }
    
    private List<String> extractImports(String code) {
        List<String> imports = new ArrayList<>();
        Pattern pattern = Pattern.compile("import\\s+([\\w.]+)\\s*;");
        Matcher matcher = pattern.matcher(code);
        
        while (matcher.find()) {
            imports.add(matcher.group(1));
        }
        
        return imports;
    }
    
    private List<String> extractClasses(String code) {
        List<String> classes = new ArrayList<>();
        Pattern pattern = Pattern.compile("(?:public\\s+)?class\\s+(\\w+)");
        Matcher matcher = pattern.matcher(code);
        
        while (matcher.find()) {
            classes.add(matcher.group(1));
        }
        
        return classes;
    }
    
    /**
     * Result of parsing operation.
     */
    public static class ParseResult {
        public String packageName;
        public List<String> imports;
        public List<String> classes;
        
        public ParseResult() {
            this.imports = new ArrayList<>();
            this.classes = new ArrayList<>();
        }
    }
}
