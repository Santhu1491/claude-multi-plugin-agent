package com.example;

import java.util.*;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.stream.Collectors;

/**
 * Sample data processing module.
 */
public class DataProcessor {
    
    public <T> List<T> filterRecords(List<T> records, Predicate<T> predicate) {
        return records.stream()
            .filter(predicate)
            .collect(Collectors.toList());
    }
    
    public <T> List<T> sortRecords(List<T> records, Comparator<T> comparator) {
        return records.stream()
            .sorted(comparator)
            .collect(Collectors.toList());
    }
    
    public <T, K> Map<K, List<T>> groupBy(List<T> records, Function<T, K> keyExtractor) {
        return records.stream()
            .collect(Collectors.groupingBy(keyExtractor));
    }
    
    public <T, R> List<R> transform(List<T> records, Function<T, R> transformer) {
        return records.stream()
            .map(transformer)
            .collect(Collectors.toList());
    }
    
    public static class Person {
        public int id;
        public String name;
        public int age;
        public String city;
        
        public Person(int id, String name, int age, String city) {
            this.id = id;
            this.name = name;
            this.age = age;
            this.city = city;
        }
        
        @Override
        public String toString() {
            return "Person{id=" + id + ", name='" + name + "', age=" + age + ", city='" + city + "'}";
        }
    }
    
    public static void main(String[] args) {
        DataProcessor processor = new DataProcessor();
        
        // Sample data
        List<Person> records = Arrays.asList(
            new Person(1, "Alice", 30, "New York"),
            new Person(2, "Bob", 25, "London"),
            new Person(3, "Charlie", 35, "New York"),
            new Person(4, "Diana", 28, "Paris")
        );
        
        System.out.println("Data Processor Demo");
        
        // Filter
        List<Person> nyResidents = processor.filterRecords(
            records, 
            p -> "New York".equals(p.city)
        );
        System.out.println("\nNew York residents: " + nyResidents.size());
        
        // Sort
        List<Person> sortedByAge = processor.sortRecords(
            records,
            Comparator.comparingInt(p -> p.age)
        );
        System.out.println("\nSorted by age: " + 
            sortedByAge.stream().map(p -> p.name).collect(Collectors.toList()));
        
        // Group
        Map<String, List<Person>> byCity = processor.groupBy(records, p -> p.city);
        System.out.println("\nGrouped by city: " + byCity.keySet());
    }
}
