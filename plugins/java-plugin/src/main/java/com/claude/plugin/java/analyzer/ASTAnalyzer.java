package com.claude.plugin.java.analyzer;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Pattern;
import java.util.regex.Matcher;

/**
 * AST analyzer for Java code.
 */
public class ASTAnalyzer {
    
    /**
     * Analyze Java code structure.
     */
    public AnalysisResult analyze(String code) {
        AnalysisResult result = new AnalysisResult();
        
        result.methods = extractMethods(code);
        result.fields = extractFields(code);
        result.complexity = calculateComplexity(code);
        result.metrics = calculateMetrics(code);
        
        return result;
    }
    
    private List<MethodInfo> extractMethods(String code) {
        List<MethodInfo> methods = new ArrayList<>();
        
        // Simple regex-based method extraction
        Pattern pattern = Pattern.compile(
            "(?:public|private|protected)?\\s+(?:static\\s+)?\\w+\\s+(\\w+)\\s*\\([^)]*\\)"
        );
        Matcher matcher = pattern.matcher(code);
        
        while (matcher.find()) {
            methods.add(new MethodInfo(matcher.group(1)));
        }
        
        return methods;
    }
    
    private List<FieldInfo> extractFields(String code) {
        List<FieldInfo> fields = new ArrayList<>();
        
        Pattern pattern = Pattern.compile(
            "(?:public|private|protected)?\\s+(?:static\\s+)?(?:final\\s+)?\\w+\\s+(\\w+)\\s*[;=]"
        );
        Matcher matcher = pattern.matcher(code);
        
        while (matcher.find()) {
            fields.add(new FieldInfo(matcher.group(1)));
        }
        
        return fields;
    }
    
    private int calculateComplexity(String code) {
        int complexity = 1;
        
        // Count control flow statements
        complexity += countOccurrences(code, "\\bif\\b");
        complexity += countOccurrences(code, "\\bfor\\b");
        complexity += countOccurrences(code, "\\bwhile\\b");
        complexity += countOccurrences(code, "\\bcase\\b");
        complexity += countOccurrences(code, "\\bcatch\\b");
        
        return complexity;
    }
    
    private Map<String, Integer> calculateMetrics(String code) {
        Map<String, Integer> metrics = new HashMap<>();
        
        metrics.put("lines", code.split("\n").length);
        metrics.put("methods", countOccurrences(code, "\\s\\w+\\s*\\([^)]*\\)\\s*\\{"));
        metrics.put("classes", countOccurrences(code, "\\bclass\\s+\\w+"));
        
        return metrics;
    }
    
    private int countOccurrences(String text, String regex) {
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(text);
        int count = 0;
        while (matcher.find()) {
            count++;
        }
        return count;
    }
    
    public static class AnalysisResult {
        public List<MethodInfo> methods;
        public List<FieldInfo> fields;
        public int complexity;
        public Map<String, Integer> metrics;
    }
    
    public static class MethodInfo {
        public String name;
        
        public MethodInfo(String name) {
            this.name = name;
        }
    }
    
    public static class FieldInfo {
        public String name;
        
        public FieldInfo(String name) {
            this.name = name;
        }
    }
}
