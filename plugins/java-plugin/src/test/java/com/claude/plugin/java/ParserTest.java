package com.claude.plugin.java;

import com.claude.plugin.java.analyzer.JavaParser;
import com.claude.plugin.java.analyzer.JavaParser.ParseResult;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Tests for JavaParser.
 */
class ParserTest {
    
    @Test
    void testParseSimpleClass() {
        JavaParser parser = new JavaParser();
        String code = """
            package com.example;
            
            public class HelloWorld {
                public static void main(String[] args) {
                    System.out.println("Hello, World!");
                }
            }
            """;
        
        ParseResult result = parser.parse(code);
        
        assertNotNull(result);
        assertEquals("com.example", result.packageName);
        assertTrue(result.classes.contains("HelloWorld"));
    }
    
    @Test
    void testParseImports() {
        JavaParser parser = new JavaParser();
        String code = """
            package com.example;
            
            import java.util.List;
            import java.util.ArrayList;
            
            public class Test {}
            """;
        
        ParseResult result = parser.parse(code);
        
        assertEquals(2, result.imports.size());
        assertTrue(result.imports.contains("java.util.List"));
        assertTrue(result.imports.contains("java.util.ArrayList"));
    }
}
