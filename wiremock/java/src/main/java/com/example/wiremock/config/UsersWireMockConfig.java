package com.example.wiremock.config;

import com.github.tomakehurst.wiremock.WireMockServer;
import com.github.tomakehurst.wiremock.core.WireMockConfiguration;
import static com.github.tomakehurst.wiremock.client.WireMock.*;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Primary;
import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;

/**
 * WireMock Configuration for Users API
 * Auto-generated from OpenAPI specification: users-api.yaml
 * Generated on: 2025-09-11 11:39:36
 * 
 * Usage in tests:
 * @SpringBootTest
 * @Import(UsersWireMockConfig.class)
 * class YourTest {
 *     @Autowired
 *     private String usersApiBaseUrl;
 * }
 */
@TestConfiguration
public class UsersWireMockConfig {

    private WireMockServer wireMockServer;
    public static final int WIREMOCK_PORT = 8089;
    
    @PostConstruct
    public void setupWireMock() {
        wireMockServer = new WireMockServer(
            WireMockConfiguration.options()
                .port(WIREMOCK_PORT)
                .usingFilesUnderClasspath("wiremock/users")
                .verbose(true)
        );
        wireMockServer.start();
        configureFor("localhost", WIREMOCK_PORT);
        setupDefaultStubs();
    }
    
    @PreDestroy
    public void tearDown() {
        if (wireMockServer != null && wireMockServer.isRunning()) {
            wireMockServer.stop();
        }
    }
    
    @Bean
    @Primary
    public String usersApiBaseUrl() {
        return "http://localhost:" + WIREMOCK_PORT;
    }
    
    @Bean
    public WireMockServer usersWireMockServer() {
        return wireMockServer;
    }
    
    private void setupDefaultStubs() {
        // Health check endpoint
        stubFor(get(urlPathEqualTo("/health"))
            .willReturn(aResponse()
                .withStatus(200)
                .withHeader("Content-Type", "application/json")
                .withBody("{\"status\": \"UP\", \"service\": \"users\"}")));
                
        // Default 404 for unmapped endpoints
        stubFor(any(urlMatching(".*"))
            .atPriority(10)
            .willReturn(aResponse()
                .withStatus(404)
                .withHeader("Content-Type", "application/json")
                .withBody("{\"error\": \"Endpoint not found\", \"service\": \"users\"}")));
    }
    
    public void resetStubs() {
        if (wireMockServer != null) {
            wireMockServer.resetAll();
            setupDefaultStubs();
        }
    }
}