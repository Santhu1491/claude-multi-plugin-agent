package com.claude.plugin.java.tools;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.regex.Pattern;
import java.nio.file.StandardOpenOption;
import java.util.List;

/**
 * Code writing utilities.
 */
public class CodeWriter {
    
    /**
     * Write content to a file.
     */
    public void writeFile(String filePath, String content) throws IOException {
        Path path = Path.of(filePath);
        Files.createDirectories(path.getParent());
        Files.writeString(path, content);
    }
    
    /**
     * Append content to a file.
     */
    public void appendToFile(String filePath, String content) throws IOException {
        Path path = Path.of(filePath);
        Files.writeString(path, content, StandardOpenOption.APPEND);
    }
    
    /**
     * Insert content at a specific line.
     */
    public void insertAtLine(String filePath, int lineNumber, String content) throws IOException {
        Path path = Path.of(filePath);
        List<String> lines = Files.readAllLines(path);
        
        if (lineNumber < 1 || lineNumber > lines.size() + 1) {
            throw new IllegalArgumentException("Invalid line number");
        }
        
        lines.add(lineNumber - 1, content);
        Files.write(path, lines);
    }
    
    /**
     * Replace text in a file.
     */
    public int replaceInFile(String filePath, String oldText, String newText) throws IOException {
        Path path = Path.of(filePath);
        String content = Files.readString(path);
        
        int count = 0;
        String temp = content;
        while (temp.contains(oldText)) {
            count++;
            temp = temp.replaceFirst(Pattern.quote(oldText), "");
        }
        
        String replaced = content.replace(oldText, newText);
        Files.writeString(path, replaced);
        
        return count;
    }
}
