package com.claude.plugin.java.utils;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * Simple logging utility.
 */
public class Logger {
    
    private static final DateTimeFormatter FORMATTER = 
        DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
    
    private final String name;
    
    public Logger(String name) {
        this.name = name;
    }
    
    public void info(String message) {
        log("INFO", message);
    }
    
    public void warning(String message) {
        log("WARNING", message);
    }
    
    public void error(String message) {
        log("ERROR", message);
    }
    
    public void debug(String message) {
        log("DEBUG", message);
    }
    
    private void log(String level, String message) {
        String timestamp = LocalDateTime.now().format(FORMATTER);
        System.out.println(String.format("%s [%s] %s: %s", 
            timestamp, level, name, message));
    }
}
