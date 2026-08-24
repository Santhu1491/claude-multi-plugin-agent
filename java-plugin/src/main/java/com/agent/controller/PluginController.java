package com.agent.controller;

import com.agent.model.PluginRequest;
import com.agent.model.PluginResponse;

public class PluginController {
    public PluginResponse execute(PluginRequest request) {
        return new PluginResponse(true, request.payload());
    }
}
