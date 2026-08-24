package com.claude.plugin.java;

import com.claude.plugin.java.execution.Executor;
import com.claude.plugin.java.execution.Executor.ExecutionResult;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Tests for Executor.
 */
class ExecutorTest {
    
    @Test
    void testExecutorInitialization() {
        Executor executor = new Executor();
        assertNotNull(executor);
    }
    
    @Test
    void testExecuteBasicCode() {
        Executor executor = new Executor();
        String code = """
            public class Test {
                public static void main(String[] args) {
                    System.out.println("Hello");
                }
            }
            """;
        
        ExecutionResult result = executor.execute(code);
        assertNotNull(result);
    }
}
