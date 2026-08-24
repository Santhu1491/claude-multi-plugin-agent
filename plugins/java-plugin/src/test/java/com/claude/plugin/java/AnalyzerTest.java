package com.claude.plugin.java;

import com.claude.plugin.java.analyzer.ASTAnalyzer;
import com.claude.plugin.java.analyzer.ASTAnalyzer.AnalysisResult;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Tests for ASTAnalyzer.
 */
class AnalyzerTest {
    
    @Test
    void testAnalyzeBasicClass() {
        ASTAnalyzer analyzer = new ASTAnalyzer();
        String code = """
            public class Calculator {
                public int add(int a, int b) {
                    return a + b;
                }
                
                public int subtract(int a, int b) {
                    return a - b;
                }
            }
            """;
        
        AnalysisResult result = analyzer.analyze(code);
        
        assertNotNull(result);
        assertTrue(result.methods.size() >= 2);
    }
    
    @Test
    void testComplexityCalculation() {
        ASTAnalyzer analyzer = new ASTAnalyzer();
        String code = """
            public class Test {
                public void method() {
                    if (true) {
                        for (int i = 0; i < 10; i++) {
                            while (true) {
                                break;
                            }
                        }
                    }
                }
            }
            """;
        
        AnalysisResult result = analyzer.analyze(code);
        
        assertTrue(result.complexity > 1);
    }
}
