package com.example.wiremock.test;

import com.example.wiremock.config.OpenApiWireMockConfig;
import com.github.tomakehurst.wiremock.WireMockServer;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit.jupiter.SpringExtension;

/**
 * Base test class for OpenApi API integration tests
 * Auto-generated from OpenAPI specification: open-api-spec.yaml
 * Generated on: 2025-09-11 11:39:36
 * 
 * Extend this class in your integration tests:
 * 
 * class OpenApiIntegrationTest extends OpenApiWireMockTest {
 *     @Test
 *     void shouldCallApi() {
 *         // Your test here using open_apiApiBaseUrl
 *         String response = restTemplate.getForObject(open_apiApiBaseUrl + "/endpoint", String.class);
 *         assertThat(response).isNotNull();
 *     }
 * }
 */
@ExtendWith(SpringExtension.class)
@SpringBootTest
@ContextConfiguration(classes = OpenApiWireMockConfig.class)
public abstract class OpenApiWireMockTest {

    @Autowired
    protected String open_apiApiBaseUrl;
    
    @Autowired
    protected WireMockServer open_apiWireMockServer;
    
    @BeforeEach
    void setUp() {
        // Reset to clean state before each test
        if (open_apiWireMockServer.isRunning()) {
            open_apiWireMockServer.resetAll();
        }
    }
    
    @AfterEach
    void tearDown() {
        // Clean up after each test
        if (open_apiWireMockServer.isRunning()) {
            open_apiWireMockServer.resetAll();
        }
    }
    
    protected String getApiBaseUrl() {
        return open_apiApiBaseUrl;
    }
    
    protected WireMockServer getWireMockServer() {
        return open_apiWireMockServer;
    }
}