package com.example;

import java.util.HashMap;
import java.util.Map;

/**
 * Sample API client implementation.
 */
public class ApiClient {
    
    private final String baseUrl;
    private final String apiKey;
    private final Map<String, String> headers;
    
    public ApiClient(String baseUrl, String apiKey) {
        this.baseUrl = baseUrl;
        this.apiKey = apiKey;
        this.headers = buildHeaders();
    }
    
    private Map<String, String> buildHeaders() {
        Map<String, String> headers = new HashMap<>();
        headers.put("Content-Type", "application/json");
        headers.put("User-Agent", "Java-API-Client/1.0");
        
        if (apiKey != null) {
            headers.put("Authorization", "Bearer " + apiKey);
        }
        
        return headers;
    }
    
    public Map<String, Object> get(String endpoint) {
        String url = baseUrl + "/" + endpoint;
        System.out.println("GET " + url);
        
        Map<String, Object> response = new HashMap<>();
        response.put("status", "success");
        response.put("data", new Object[]{});
        return response;
    }
    
    public Map<String, Object> post(String endpoint, Map<String, Object> data) {
        String url = baseUrl + "/" + endpoint;
        System.out.println("POST " + url);
        
        Map<String, Object> response = new HashMap<>();
        response.put("status", "created");
        response.put("data", data);
        return response;
    }
    
    public Map<String, Object> put(String endpoint, Map<String, Object> data) {
        String url = baseUrl + "/" + endpoint;
        System.out.println("PUT " + url);
        
        Map<String, Object> response = new HashMap<>();
        response.put("status", "updated");
        response.put("data", data);
        return response;
    }
    
    public Map<String, Object> delete(String endpoint) {
        String url = baseUrl + "/" + endpoint;
        System.out.println("DELETE " + url);
        
        Map<String, Object> response = new HashMap<>();
        response.put("status", "deleted");
        return response;
    }
    
    public static void main(String[] args) {
        ApiClient client = new ApiClient("https://api.example.com", "test-api-key");
        
        System.out.println("API Client Demo");
        client.get("users");
        
        Map<String, Object> userData = new HashMap<>();
        userData.put("name", "John Doe");
        userData.put("email", "john@example.com");
        client.post("users", userData);
        
        Map<String, Object> updateData = new HashMap<>();
        updateData.put("name", "Jane Doe");
        client.put("users/1", updateData);
        
        client.delete("users/1");
    }
}
