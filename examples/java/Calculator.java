package com.example;

/**
 * Simple calculator implementation.
 */
public class Calculator {
    
    public double add(double a, double b) {
        return a + b;
    }
    
    public double subtract(double a, double b) {
        return a - b;
    }
    
    public double multiply(double a, double b) {
        return a * b;
    }
    
    public double divide(double a, double b) {
        if (b == 0) {
            throw new IllegalArgumentException("Cannot divide by zero");
        }
        return a / b;
    }
    
    public double power(double base, double exponent) {
        return Math.pow(base, exponent);
    }
    
    public static void main(String[] args) {
        Calculator calc = new Calculator();
        
        System.out.println("Calculator Demo");
        System.out.println("10 + 5 = " + calc.add(10, 5));
        System.out.println("10 - 5 = " + calc.subtract(10, 5));
        System.out.println("10 * 5 = " + calc.multiply(10, 5));
        System.out.println("10 / 5 = " + calc.divide(10, 5));
        System.out.println("2 ^ 8 = " + calc.power(2, 8));
    }
}
