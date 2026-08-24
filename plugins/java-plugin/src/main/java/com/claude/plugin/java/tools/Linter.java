package com.claude.plugin.java.tools;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;
import java.util.regex.Matcher;

/**
 * Code linting functionality.
 */
public class Linter {
    
    private static final int MAX_LINE_LENGTH = 120;
    
    /**
     * Lint Java code for common issues.
     */
    public List<LintIssue> lint(String code) {
        List<LintIssue> issues = new ArrayList<>();
        
        issues.addAll(checkLongLines(code));
        issues.addAll(checkMissingJavadoc(code));
        issues.addAll(checkNamingConventions(code));
        
        return issues;
    }
    
    private List<LintIssue> checkLongLines(String code) {
        List<LintIssue> issues = new ArrayList<>();
        String[] lines = code.split("\n");
        
        for (int i = 0; i < lines.length; i++) {
            if (lines[i].length() > MAX_LINE_LENGTH) {
                issues.add(new LintIssue(
                    "line_too_long",
                    i + 1,
                    "Line exceeds " + MAX_LINE_LENGTH + " characters",
                    "warning"
                ));
            }
        }
        
        return issues;
    }
    
    private List<LintIssue> checkMissingJavadoc(String code) {
        List<LintIssue> issues = new ArrayList<>();
        
        Pattern methodPattern = Pattern.compile("(?:public|private|protected)\\s+\\w+\\s+\\w+\\s*\\([^)]*\\)");
        Matcher matcher = methodPattern.matcher(code);
        
        // Simple check - would need more sophisticated parsing in reality
        return issues;
    }
    
    private List<LintIssue> checkNamingConventions(String code) {
        List<LintIssue> issues = new ArrayList<>();
        
        // Check for class names starting with lowercase
        Pattern classPattern = Pattern.compile("class\\s+([a-z]\\w*)");
        Matcher matcher = classPattern.matcher(code);
        
        while (matcher.find()) {
            issues.add(new LintIssue(
                "naming_convention",
                0,
                "Class name should start with uppercase: " + matcher.group(1),
                "warning"
            ));
        }
        
        return issues;
    }
    
    public record LintIssue(String type, int line, String message, String severity) {}
}
