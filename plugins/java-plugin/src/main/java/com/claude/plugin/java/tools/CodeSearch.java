package com.claude.plugin.java.tools;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.util.stream.Collectors;

/**
 * Code search functionality.
 */
public class CodeSearch {
    
    /**
     * Search for a pattern in Java files.
     */
    public List<SearchResult> search(String query, String rootPath) throws IOException {
        List<SearchResult> results = new ArrayList<>();
        Path root = Path.of(rootPath);
        
        List<Path> javaFiles = Files.walk(root)
            .filter(p -> p.toString().endsWith(".java"))
            .collect(Collectors.toList());
        
        for (Path file : javaFiles) {
            results.addAll(searchFile(file, query));
        }
        
        return results;
    }
    
    private List<SearchResult> searchFile(Path filePath, String query) throws IOException {
        List<SearchResult> results = new ArrayList<>();
        List<String> lines = Files.readAllLines(filePath);
        
        Pattern pattern = Pattern.compile(query, Pattern.CASE_INSENSITIVE);
        
        for (int i = 0; i < lines.size(); i++) {
            Matcher matcher = pattern.matcher(lines.get(i));
            if (matcher.find()) {
                results.add(new SearchResult(
                    filePath.toString(),
                    i + 1,
                    lines.get(i).trim()
                ));
            }
        }
        
        return results;
    }
    
    public record SearchResult(String file, int line, String content) {}
}
