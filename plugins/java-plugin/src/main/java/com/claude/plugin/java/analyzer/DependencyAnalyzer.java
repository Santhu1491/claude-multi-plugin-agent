package com.claude.plugin.java.analyzer;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import java.util.stream.Collectors;
import java.util.regex.Pattern;
import java.util.regex.Matcher;

/**
 * Dependency analyzer for Java projects.
 */
public class DependencyAnalyzer {
    
    /**
     * Analyze dependencies in a Java project.
     */
    public DependencyResult analyzeProject(String rootPath) throws IOException {
        Path root = Path.of(rootPath);
        List<Path> javaFiles = Files.walk(root)
            .filter(p -> p.toString().endsWith(".java"))
            .collect(Collectors.toList());
        
        Set<String> allImports = new HashSet<>();
        Map<String, List<String>> fileDependencies = new HashMap<>();
        
        for (Path javaFile : javaFiles) {
            String code = Files.readString(javaFile);
            List<String> imports = extractImports(code);
            
            fileDependencies.put(javaFile.toString(), imports);
            allImports.addAll(imports);
        }
        
        return new DependencyResult(
            rootPath,
            javaFiles.size(),
            allImports.size(),
            new ArrayList<>(allImports),
            fileDependencies
        );
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
    
    public record DependencyResult(
        String rootPath,
        int filesAnalyzed,
        int uniqueImports,
        List<String> allImports,
        Map<String, List<String>> fileDependencies
    ) {}
}
