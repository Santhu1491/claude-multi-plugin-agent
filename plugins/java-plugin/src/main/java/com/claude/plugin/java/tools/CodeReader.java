package com.claude.plugin.java.tools;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

/**
 * Code reading utilities.
 */
public class CodeReader {
    
    /**
     * Read a Java file.
     */
    public String readFile(String filePath) throws IOException {
        return Files.readString(Path.of(filePath));
    }
    
    /**
     * Read specific lines from a file.
     */
    public String readLines(String filePath, int start, int end) throws IOException {
        List<String> lines = Files.readAllLines(Path.of(filePath));
        
        if (start < 1 || end > lines.size() || start > end) {
            throw new IllegalArgumentException("Invalid line range");
        }
        
        return String.join("\n", lines.subList(start - 1, end));
    }
    
    /**
     * Get file information.
     */
    public FileInfo getFileInfo(String filePath) throws IOException {
        Path path = Path.of(filePath);
        
        if (!Files.exists(path)) {
            throw new IOException("File not found: " + filePath);
        }
        
        long size = Files.size(path);
        long lines = Files.lines(path).count();
        
        return new FileInfo(filePath, size, lines);
    }
    
    public record FileInfo(String path, long size, long lines) {}
}
