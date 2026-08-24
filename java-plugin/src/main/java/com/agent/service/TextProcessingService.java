package com.agent.service;

public class TextProcessingService {
    public int wordCount(String text) {
        return text == null || text.isBlank() ? 0 : text.trim().split("\\s+").length;
    }
}
