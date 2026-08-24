package com.example;

/**
 * Sample Java application for testing the plugin.
 */
public class SampleApp {
    
    public static void main(String[] args) {
        System.out.println("Sample Java Application");
        
        // Demonstrate basic functionality
        int result = calculate(10, 20);
        System.out.println("Calculation result: " + result);
        
        // Process some data
        processData("John Doe", 30);
    }
    
    private static int calculate(int a, int b) {
        return a + b;
    }
    
    private static void processData(String name, int age) {
        System.out.println("Processing data:");
        System.out.println("  Name: " + name);
        System.out.println("  Age: " + age);
    }
}
