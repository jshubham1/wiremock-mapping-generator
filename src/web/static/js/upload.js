// Global variables
let selectedFiles = [];
let currentSessionId = window.SESSION_ID || ''; // Get session ID from template

// DOM elements
let dropZone, fileInput, fileList, fileItems, generateBtn, uploadForm;
let progressModal, successModal, progressBar, progressText;
let outputTypeRadios, javaOptions;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    dropZone = document.getElementById('dropZone');
    fileInput = document.getElementById('fileInput');
    fileList = document.getElementById('fileList');
    fileItems = document.getElementById('fileItems');
    generateBtn = document.getElementById('generateBtn');
    uploadForm = document.getElementById('uploadForm');
    
    progressModal = document.getElementById('progressModal');
    successModal = document.getElementById('successModal');
    progressBar = document.getElementById('progressBar');
    progressText = document.getElementById('progressText');
    
    outputTypeRadios = document.querySelectorAll('input[name="outputType"]');
    javaOptions = document.getElementById('javaOptions');
    
    if (!dropZone || !fileInput) {
        console.error('❌ Required elements not found!');
        return;
    }
    
    // Initialize event listeners
    initializeEventListeners();
});

function initializeEventListeners() {
    // Setup event listeners for upload functionality
    
    // Prevent default drag behaviors on the entire page
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        document.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });
    
    // Drop zone events
    dropZone.addEventListener('click', handleDropZoneClick, false);
    dropZone.addEventListener('dragenter', handleDragEnter, false);
    dropZone.addEventListener('dragover', handleDragOver, false);
    dropZone.addEventListener('dragleave', handleDragLeave, false);
    dropZone.addEventListener('drop', handleDrop, false);
    
    // File input change
    fileInput.addEventListener('change', handleFileSelect);
    
    // Form submission
    uploadForm.addEventListener('submit', handleFormSubmit);
    
    // Option changes
    outputTypeRadios.forEach(radio => {
        radio.addEventListener('change', handleOutputTypeChange);
    });
    
    // Modal buttons
    if (document.getElementById('downloadBtn')) {
        document.getElementById('downloadBtn').addEventListener('click', handleDownload);
    }
    
    if (document.getElementById('newGenerationBtn')) {
        document.getElementById('newGenerationBtn').addEventListener('click', handleNewGeneration);
    }
    
}

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function handleDropZoneClick(e) {
    
    // For Chrome compatibility, we need to trigger the file input
    // immediately and synchronously without any complex operations
    if (fileInput) {
        // Don't prevent default or stop propagation for file input clicks
        fileInput.click();
    } else {
        console.error('❌ File input not found');
    }
}

function handleDragEnter(e) {
    preventDefaults(e);
    dropZone.classList.add('drag-over');
}

function handleDragOver(e) {
    preventDefaults(e);
    dropZone.classList.add('drag-over');
}

function handleDragLeave(e) {
    preventDefaults(e);
    
    // Only remove drag-over if we're actually leaving the dropZone
    const rect = dropZone.getBoundingClientRect();
    const x = e.clientX;
    const y = e.clientY;
    
    if (x < rect.left || x > rect.right || y < rect.top || y > rect.bottom) {
        dropZone.classList.remove('drag-over');
    }
}

function handleDrop(e) {
    preventDefaults(e);
    dropZone.classList.remove('drag-over');
    
    const files = Array.from(e.dataTransfer.files);
    
    processFiles(files);
}

function handleFileSelect(e) {
    const files = Array.from(e.target.files);
    
    processFiles(files);
}

function processFiles(files) {
    
    const validFiles = files.filter(file => {
        const extension = file.name.toLowerCase().split('.').pop();
        const isValid = ['yaml', 'yml', 'json'].includes(extension);
        
        if (!isValid) {
            console.warn(`❌ Invalid file type: ${file.name}`);
        }
        
        return isValid;
    });
    
    
    selectedFiles = validFiles;
    updateFileList();
    updateGenerateButton();
}

function updateFileList() {
    
    if (selectedFiles.length === 0) {
        fileList.classList.add('hidden');
        return;
    }
    
    fileList.classList.remove('hidden');
    fileItems.innerHTML = '';
    
    selectedFiles.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'flex items-center justify-between p-3 bg-gray-50 rounded-lg';
        
        const extension = file.name.toLowerCase().split('.').pop();
        const iconClass = extension === 'json' ? 'text-blue-600' : 'text-openapi';
        
        fileItem.innerHTML = `
            <div class="flex items-center">
                <i class="fas fa-file-code ${iconClass} mr-3"></i>
                <div>
                    <div class="font-medium text-gray-900">${file.name}</div>
                    <div class="text-sm text-gray-500">${formatFileSize(file.size)}</div>
                </div>
            </div>
            <button type="button" onclick="removeFile(${index})" class="text-red-600 hover:text-red-800">
                <i class="fas fa-trash"></i>
            </button>
        `;
        fileItems.appendChild(fileItem);
    });
}

function updateGenerateButton() {
    const hasFiles = selectedFiles.length > 0;
    generateBtn.disabled = !hasFiles;
    
}

function removeFile(index) {
    selectedFiles.splice(index, 1);
    updateFileList();
    updateGenerateButton();
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function handleOutputTypeChange(e) {
    const showJavaOptions = e.target.value === 'json-java';
    
    if (showJavaOptions) {
        javaOptions.classList.remove('hidden');
    } else {
        javaOptions.classList.add('hidden');
    }
    
}

async function handleFormSubmit(e) {
    e.preventDefault();
    
    if (selectedFiles.length === 0) {
        console.warn('❌ No files selected');
        return;
    }
    
    try {
        await uploadAndGenerate();
    } catch (error) {
        console.error('❌ Upload/generation failed:', error);
        hideProgressModal();
        alert('Error: ' + error.message);
    }
}

async function uploadAndGenerate() {
    
    // Show progress modal
    showProgressModal();
    updateProgress(0, 'Preparing files...');
    
    // Create form data
    const formData = new FormData();
    formData.append('session_id', currentSessionId);
    
    selectedFiles.forEach(file => {
        formData.append('files', file);
    });
    
    const outputType = document.querySelector('input[name="outputType"]:checked').value;
    formData.append('generateJava', outputType === 'json-java');
    formData.append('javaPackage', document.getElementById('javaPackage').value);
    
    // Upload files
    updateProgress(25, 'Uploading files...');
    
    const uploadResponse = await fetch('/api/upload', {
        method: 'POST',
        body: formData
    });
    
    if (!uploadResponse.ok) {
        const error = await uploadResponse.json();
        throw new Error(error.error || 'Upload failed');
    }
    
    const uploadResult = await uploadResponse.json();
    // Session ID should remain the same
    currentSessionId = uploadResult.session_id;
    
    // Generate mappings
    updateProgress(50, 'Generating mappings...');
    
    const generateResponse = await fetch('/api/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            session_id: currentSessionId,
            include_java: outputType === 'json-java'
        })
    });
    
    if (!generateResponse.ok) {
        const error = await generateResponse.json();
        throw new Error(error.error || 'Generation failed');
    }
    
    const generateResult = await generateResponse.json();
    
    // Upload mappings to WireMock server
    updateProgress(75, 'Uploading mappings to WireMock...');
    
    try {
        await uploadMappingsToWireMock(currentSessionId);
        updateProgress(100, 'Complete!');
    } catch (error) {
        console.warn('⚠️ Failed to upload mappings to WireMock:', error);
        updateProgress(100, 'Complete! (Manual WireMock upload needed)');
    }
    
    setTimeout(() => {
        hideProgressModal();
        showSuccessModal({
            uploadedFiles: uploadResult.files,
            generatedMappings: generateResult.results.reduce((total, r) => total + (r.mappings_generated || 0), 0),
            responseFiles: generateResult.results.length * 6,
            includeJava: generateResult.include_java,
            javaFiles: generateResult.include_java ? generateResult.results.length * 4 : 0,
            zipSize: 1024 * 50 // Placeholder
        });
    }, 1000);
}

function showProgressModal() {
    progressModal.classList.remove('hidden');
}

function hideProgressModal() {
    progressModal.classList.add('hidden');
}

function updateProgress(percent, text) {
    progressBar.style.width = percent + '%';
    progressText.textContent = text;
}

function showSuccessModal(summary) {
    // Populate summary stats
    const summaryContent = document.getElementById('summaryContent');
    summaryContent.innerHTML = `
        <div class="bg-white p-4 rounded-lg border border-gray-200">
            <div class="text-center">
                <div class="text-2xl font-bold text-gray-900">${summary.uploadedFiles.length}</div>
                <div class="text-sm text-gray-600">Files Processed</div>
            </div>
        </div>
        <div class="bg-white p-4 rounded-lg border border-gray-200">
            <div class="text-center">
                <div class="text-2xl font-bold text-wiremock">${summary.generatedMappings}</div>
                <div class="text-sm text-gray-600">Mappings Created</div>
            </div>
        </div>
        <div class="bg-white p-4 rounded-lg border border-gray-200">
            <div class="text-center">
                <div class="text-2xl font-bold text-blue-600">${summary.responseFiles}</div>
                <div class="text-sm text-gray-600">Response Files</div>
            </div>
        </div>
        <div class="bg-white p-4 rounded-lg border border-gray-200">
            <div class="text-center">
                <div class="text-2xl font-bold text-green-600">${formatFileSize(summary.zipSize)}</div>
                <div class="text-sm text-gray-600">Package Size</div>
            </div>
        </div>
    `;
    
    // Populate generation summary
    const generationSummary = document.getElementById('generation-summary');
    generationSummary.innerHTML = `
        <div><strong>Uploaded files:</strong> ${summary.uploadedFiles.length}</div>
        <div><strong>Generated mappings:</strong> ${summary.generatedMappings}</div>
        <div><strong>Response files:</strong> ${summary.responseFiles}</div>
        ${summary.includeJava ? `<div><strong>Java files:</strong> ${summary.javaFiles}</div>` : ''}
        <div><strong>Package size:</strong> ${formatFileSize(summary.zipSize)}</div>
        <div class="mt-3 pt-3 border-t border-gray-200">
            <div class="text-xs text-gray-500">Session ID: ${currentSessionId}</div>
        </div>
    `;
    
    // Store summary data globally for other tabs
    window.mappingSummary = summary;
    
    // Populate mappings list
    populateMappingsList(summary);
    
    // Populate test endpoints
    populateTestEndpoints(summary);
    
    successModal.classList.remove('hidden');
}

function handleDownload() {
    if (currentSessionId) {
        window.location.href = `/api/download/${currentSessionId}`;
    }
}

function handleNewGeneration() {
    successModal.classList.add('hidden');
    selectedFiles = [];
    updateFileList();
    updateGenerateButton();
    fileInput.value = '';
    currentSessionId = '';
}

// Export functions for global access
window.removeFile = removeFile;
window.showTab = showTab;
window.closeResultsModal = closeResultsModal;
window.startWireMockInstance = startWireMockInstance;
window.testWireMockHealth = testWireMockHealth;
window.executeTest = executeTest;
window.uploadMappingsToWireMock = uploadMappingsToWireMock;

// Function to upload generated mappings to WireMock server
async function uploadMappingsToWireMock(sessionId) {
    const wiremockUrl = 'http://localhost:8080';
    
    try {
        
        // First, get the generated mappings from our Flask backend
        const mappingsResponse = await fetch(`/api/mappings/${sessionId}`);
        
        if (!mappingsResponse.ok) {
            const errorText = await mappingsResponse.text();
            console.error(`❌ Failed to get mappings: ${mappingsResponse.status} - ${errorText}`);
            throw new Error(`Failed to get generated mappings: ${errorText}`);
        }
        
        const mappingsData = await mappingsResponse.json();
        
        if (!mappingsData.mappings || mappingsData.mappings.length === 0) {
            console.warn('⚠️ No mappings found to upload - this might be why WireMock shows 0 mappings');
            // Continue with response files if they exist
        } else {
            // Upload each mapping to WireMock
            let uploadedCount = 0;
            let failedCount = 0;
            
            for (const [index, mapping] of mappingsData.mappings.entries()) {
                try {
                    
                    const uploadResponse = await fetch(`${wiremockUrl}/__admin/mappings`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            ...mapping,
                            response: {
                                ...mapping.response,
                                headers: {
                                    ...mapping.response.headers,
                                    "Access-Control-Allow-Origin": "*",
                                    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                                    "Access-Control-Allow-Headers": "Content-Type, Authorization, Accept"
                                }
                            }
                        })
                    });
                    
                    if (uploadResponse.ok) {
                        uploadedCount++;
                        const result = await uploadResponse.json();
                    } else {
                        failedCount++;
                        const errorText = await uploadResponse.text();
                        console.warn(`⚠️ Failed to upload mapping: ${mapping.request.method} ${mapping.request.url || mapping.request.urlPattern}`);
                        console.warn(`   Error: ${uploadResponse.status} - ${errorText}`);
                    }
                } catch (error) {
                    failedCount++;
                    console.warn(`⚠️ Error uploading mapping ${index + 1}: ${error.message}`);
                }
            }
            
        }
        
        // Also upload response files if they exist
        if (mappingsData.responseFiles && Object.keys(mappingsData.responseFiles).length > 0) {
            await uploadResponseFiles(wiremockUrl, mappingsData.responseFiles);
        } else {
        }
        
        return mappingsData.mappings?.length || 0;
        
    } catch (error) {
        console.error('❌ Failed to upload mappings to WireMock:', error);
        throw error;
    }
}

// Helper function to upload response files
async function uploadResponseFiles(wiremockUrl, responseFiles) {
    
    for (const [fileName, content] of Object.entries(responseFiles)) {
        try {
            const uploadResponse = await fetch(`${wiremockUrl}/__admin/files/${fileName}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: content
            });
            
            if (uploadResponse.ok) {
            } else {
                console.warn(`⚠️ Failed to upload response file: ${fileName}`);
            }
        } catch (error) {
            console.warn(`⚠️ Error uploading response file ${fileName}: ${error.message}`);
        }
    }
}
window.showAllMappings = showAllMappings;

// Tab management
function showTab(tabName) {
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.add('hidden');
    });
    
    // Remove active class from all tabs
    document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.remove('active');
        button.classList.add('text-gray-500', 'border-transparent');
        button.classList.remove('text-wiremock', 'border-wiremock');
    });
    
    // Show selected tab content
    document.getElementById(`${tabName}-content`).classList.remove('hidden');
    
    // Activate selected tab
    const activeTab = document.getElementById(`tab-${tabName}`);
    activeTab.classList.add('active', 'text-wiremock', 'border-wiremock');
    activeTab.classList.remove('text-gray-500', 'border-transparent');
}

function closeResultsModal() {
    successModal.classList.add('hidden');
}

// WireMock instance management
function startWireMockInstance() {
    const instructions = `
To start a WireMock instance with your generated mappings:

1. Extract the downloaded ZIP file
2. Navigate to the extracted directory
3. Run one of these commands:

**Using Docker (Recommended):**
docker run -it --rm -p 8080:8080 -v "$PWD:/home/wiremock" wiremock/wiremock:latest

**Using Java:**
java -jar wiremock-standalone.jar --port 8080 --root-dir .

**Using Maven:**
mvn exec:java -Dexec.mainClass="com.github.tomakehurst.wiremock.standalone.WireMockServerRunner" -Dexec.args="--port 8080"

Your WireMock instance will be available at http://localhost:8080
Admin UI: http://localhost:8080/__admin
    `;
    
    alert(instructions);
}

// Health check functionality
async function testWireMockHealth() {
    const url = document.getElementById('wiremock-url').value;
    const statusDiv = document.getElementById('health-status');
    
    try {
        statusDiv.innerHTML = '<i class="fas fa-spinner fa-spin text-blue-600"></i> Testing connection...';
        
        const response = await fetch(`${url}/__admin/health`);
        
        if (response.ok) {
            statusDiv.innerHTML = '<i class="fas fa-check-circle text-green-600"></i> WireMock is running!';
        } else {
            statusDiv.innerHTML = '<i class="fas fa-exclamation-circle text-yellow-600"></i> WireMock responded but may have issues';
        }
    } catch (error) {
        statusDiv.innerHTML = '<i class="fas fa-times-circle text-red-600"></i> Cannot connect to WireMock. Make sure it\'s running.';
    }
}

// Mappings list population
async function populateMappingsList(summary) {
    const mappingsList = document.getElementById('mappings-list');
    
    try {
        // Try to get real mappings from WireMock server
        const response = await fetch('http://localhost:8080/__admin/mappings');
        
        if (response.ok) {
            const data = await response.json();
            const mappings = data.mappings || [];
            
            if (mappings.length > 0) {
                displayRealMappings(mappings, mappingsList);
                return;
            }
        }
    } catch (error) {
        console.warn('⚠️ Could not fetch real mappings from WireMock, showing mock data:', error);
    }
    
    // Fallback to mock data
    const mappings = generateMockMappings(summary);
    displayMockMappings(mappings, mappingsList);
}

function displayRealMappings(mappings, container) {
    // Group mappings by API/spec
    const groupedMappings = groupMappingsBySpec(mappings);
    
    container.innerHTML = Object.entries(groupedMappings).map(([specName, specMappings]) => {
        const isExpanded = Object.keys(groupedMappings).length === 1; // Auto-expand if only one API
        
        return `
            <div class="api-group mb-6">
                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg cursor-pointer" onclick="toggleMappingGroup('${specName}')">
                    <div class="flex items-center space-x-3">
                        <i class="fas fa-api text-wiremock"></i>
                        <div>
                            <h4 class="font-medium text-gray-900">${specName}</h4>
                            <p class="text-sm text-gray-600">${specMappings.length} mappings</p>
                        </div>
                    </div>
                    <i class="fas fa-chevron-${isExpanded ? 'up' : 'down'} text-gray-400" id="chevron-${specName}"></i>
                </div>
                <div class="mapping-group-content mt-3 space-y-3 ${isExpanded ? '' : 'hidden'}" id="group-${specName}">
                    ${specMappings.slice(0, 10).map(mapping => createRealMappingCard(mapping)).join('')}
                    ${specMappings.length > 10 ? `
                        <div class="text-center">
                            <button onclick="showAllMappings('${specName}')" class="text-blue-600 hover:text-blue-800 text-sm">
                                Show ${specMappings.length - 10} more mappings
                            </button>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }).join('');
}

function displayMockMappings(mappings, container) {
    // Group by API name for better organization
    const groupedMappings = groupMappingsByAPI(mappings);
    
    container.innerHTML = Object.keys(groupedMappings).map(apiName => `
        <div class="mb-6">
            <h5 class="font-semibold text-gray-900 mb-3 flex items-center">
                <i class="fas fa-file-code text-wiremock mr-2"></i>
                ${apiName}
                <span class="ml-2 text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded-full">${groupedMappings[apiName].length} mappings</span>
            </h5>
            <div class="space-y-2">
                ${groupedMappings[apiName].slice(0, 10).map(mapping => createMockMappingCard(mapping)).join('')}
                ${groupedMappings[apiName].length > 10 ? `
                    <div class="text-center py-2">
                        <button onclick="showAllMappings('${apiName}')" class="text-wiremock hover:text-orange-600 text-sm">
                            Show ${groupedMappings[apiName].length - 10} more mappings...
                        </button>
                    </div>
                ` : ''}
            </div>
        </div>
    `).join('');
    
    // Store mappings globally for filtering
    window.allMappings = mappings;
}

function groupMappingsBySpec(mappings) {
    const grouped = {};
    
    mappings.forEach(mapping => {
        // Try to determine API name from the mapping
        let specName = 'Unknown API';
        
        // Look for API name in the URL path
        if (mapping.request && mapping.request.url) {
            const pathParts = mapping.request.url.split('/').filter(p => p);
            if (pathParts.length > 0) {
                specName = pathParts[0];
            }
        }
        
        // Try to get from metadata if available
        if (mapping.metadata && mapping.metadata.apiName) {
            specName = mapping.metadata.apiName;
        }
        
        if (!grouped[specName]) {
            grouped[specName] = [];
        }
        grouped[specName].push(mapping);
    });
    
    return grouped;
}

function createRealMappingCard(mapping) {
    const method = mapping.request.method || 'GET';
    const url = mapping.request.url || mapping.request.urlPattern || '/';
    const status = mapping.response.status || 200;
    const id = mapping.id || 'unknown';
    
    return `
        <div class="mapping-card bg-white border border-gray-200 rounded-lg p-4">
            <div class="flex items-start justify-between">
                <div class="flex-1">
                    <div class="flex items-center space-x-3 mb-2">
                        <span class="inline-flex items-center px-2 py-1 rounded text-xs font-medium ${getMethodColor(method)}">
                            ${method}
                        </span>
                        <code class="text-sm text-gray-700">${url}</code>
                    </div>
                    <div class="flex items-center space-x-4 text-xs text-gray-500">
                        <span><i class="fas fa-code mr-1"></i>Status: ${status}</span>
                        <span><i class="fas fa-tag mr-1"></i>ID: ${id.substring(0, 8)}...</span>
                    </div>
                </div>
                <div class="flex items-center space-x-2">
                    <button onclick="copyMappingUrl('http://localhost:8080${url}')" class="text-gray-400 hover:text-gray-600" title="Copy URL">
                        <i class="fas fa-copy"></i>
                    </button>
                    <button onclick="testMapping('http://localhost:8080${url}', '${method}')" class="text-blue-400 hover:text-blue-600" title="Test">
                        <i class="fas fa-play"></i>
                    </button>
                </div>
            </div>
        </div>
    `;
}

function createMockMappingCard(mapping) {
    return `
        <div class="mapping-card bg-white border border-gray-200 rounded-lg p-3">
            <div class="flex items-start justify-between">
                <div class="flex-1">
                    <div class="flex items-center space-x-3 mb-2">
                        <span class="inline-flex items-center px-2 py-1 rounded text-xs font-medium ${getMethodColor(mapping.method)}">
                            ${mapping.method}
                        </span>
                        <code class="text-sm text-gray-700">${mapping.path}</code>
                        <span class="text-xs text-gray-500">${mapping.status}</span>
                    </div>
                    <div class="text-sm text-gray-600 mb-1">${mapping.description}</div>
                    <div class="flex items-center space-x-4 text-xs text-gray-500">
                        <span><i class="fas fa-tag mr-1"></i>${mapping.scenario}</span>
                        <span><i class="fas fa-code mr-1"></i>${mapping.operationId}</span>
                    </div>
                </div>
                <div class="flex items-center space-x-2">
                    <button onclick="copyMappingUrl('${mapping.fullUrl}')" class="text-gray-400 hover:text-gray-600" title="Copy URL">
                        <i class="fas fa-copy"></i>
                    </button>
                    <button onclick="testMapping('${mapping.fullUrl}', '${mapping.method}')" class="text-blue-400 hover:text-blue-600" title="Test">
                        <i class="fas fa-play"></i>
                    </button>
                </div>
            </div>
        </div>
    `;
}

// Helper functions for mapping groups
window.toggleMappingGroup = function(groupName) {
    const content = document.getElementById(`group-${groupName}`);
    const chevron = document.getElementById(`chevron-${groupName}`);
    
    if (content && chevron) {
        if (content.classList.contains('hidden')) {
            content.classList.remove('hidden');
            chevron.classList.remove('fa-chevron-down');
            chevron.classList.add('fa-chevron-up');
        } else {
            content.classList.add('hidden');
            chevron.classList.remove('fa-chevron-up');
            chevron.classList.add('fa-chevron-down');
        }
    }
};

window.showAllMappings = function(groupName) {
    // This would expand to show all mappings - implementation depends on UI needs
    showNotification(`Showing all mappings for ${groupName}`, 'info');
};

function groupMappingsByAPI(mappings) {
    return mappings.reduce((groups, mapping) => {
        const apiName = mapping.apiName;
        if (!groups[apiName]) {
            groups[apiName] = [];
        }
        groups[apiName].push(mapping);
        return groups;
    }, {});
}

function generateMockMappings(summary) {
    const scenarios = ['success', 'unauthorized', 'forbidden', 'not_found', 'server_error', 'bad_gateway', 'service_unavailable'];
    const methods = ['GET', 'POST', 'PUT', 'DELETE'];
    const mappings = [];
    
    
    // Generate mappings for each uploaded file
    summary.uploadedFiles.forEach((file, fileIndex) => {
        const apiName = file.name.replace(/\.(yaml|yml|json)$/, '');
        const cleanApiName = apiName.toLowerCase().replace(/[^a-z0-9]/g, '');
        
        
        // Generate different endpoints for each API based on common patterns
        const endpoints = [
            { path: `/${cleanApiName}`, description: `Get ${apiName} list` },
            { path: `/${cleanApiName}/{id}`, description: `Get ${apiName} by ID` },
            { path: `/${cleanApiName}`, description: `Create ${apiName}` },
            { path: `/${cleanApiName}/{id}`, description: `Update ${apiName}` },
            { path: `/${cleanApiName}/{id}`, description: `Delete ${apiName}` },
            { path: `/${cleanApiName}/search`, description: `Search ${apiName}` },
            { path: `/${cleanApiName}/metadata`, description: `Get ${apiName} metadata` },
            { path: `/${cleanApiName}/validate`, description: `Validate ${apiName}` }
        ];
        
        // Create mappings for each endpoint and method combination
        endpoints.forEach((endpoint, endpointIndex) => {
            const appropriateMethods = getMethodsForEndpoint(endpoint.path, endpoint.description);
            
            appropriateMethods.forEach(method => {
                scenarios.forEach((scenario, scenarioIndex) => {
                    const status = getStatusForScenario(scenario);
                    const mappingId = `${apiName}_${method}_${endpointIndex}_${scenarioIndex}`;
                    
                    mappings.push({
                        id: mappingId,
                        method,
                        path: endpoint.path,
                        fullUrl: `http://localhost:8080${endpoint.path}`,
                        description: `${endpoint.description} - ${scenario} scenario`,
                        scenario,
                        status,
                        operationId: `${method.toLowerCase()}${apiName.replace(/[^a-zA-Z0-9]/g, '')}`,
                        apiName: apiName,
                        fileIndex: fileIndex
                    });
                });
            });
        });
    });
    
    return mappings;
}

function getMethodsForEndpoint(path, description) {
    if (description.toLowerCase().includes('create')) return ['POST'];
    if (description.toLowerCase().includes('update')) return ['PUT', 'PATCH'];
    if (description.toLowerCase().includes('delete')) return ['DELETE'];
    if (description.toLowerCase().includes('get') || description.toLowerCase().includes('list') || description.toLowerCase().includes('search')) return ['GET'];
    if (path.includes('{id}')) return ['GET', 'PUT', 'DELETE'];
    return ['GET', 'POST'];
}

function getStatusForScenario(scenario) {
    const statusMap = {
        'success': 200,
        'unauthorized': 401,
        'forbidden': 403,
        'not_found': 404,
        'server_error': 500,
        'bad_gateway': 502,
        'service_unavailable': 503
    };
    return statusMap[scenario] || 200;
}

function getMethodColor(method) {
    const colors = {
        'GET': 'bg-blue-100 text-blue-800',
        'POST': 'bg-green-100 text-green-800',
        'PUT': 'bg-yellow-100 text-yellow-800',
        'DELETE': 'bg-red-100 text-red-800'
    };
    return colors[method] || 'bg-gray-100 text-gray-800';
}

function copyMappingUrl(url) {
    navigator.clipboard.writeText(url).then(() => {
        showNotification('URL copied to clipboard!', 'success');
    });
}

async function testMapping(url, method) {
    try {
        // Replace URL patterns with sample values for testing
        let testUrl = url;
        if (testUrl.includes('{id}')) {
            testUrl = testUrl.replace('{id}', '123');
        }
        if (testUrl.includes('{userId}')) {
            testUrl = testUrl.replace('{userId}', 'user123');
        }
        if (testUrl.includes('{accountId}')) {
            testUrl = testUrl.replace('{accountId}', 'acc123');
        }
        // Replace any remaining patterns with sample values
        testUrl = testUrl.replace(/\{([^}]+)\}/g, 'sample-$1');
        
        const response = await fetch(testUrl, { 
            method,
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        });
        const result = `${method} ${testUrl}\nStatus: ${response.status}\nResponse: ${await response.text()}`;
        showNotification(`Test completed: ${response.status}`, response.ok ? 'success' : 'error');
    } catch (error) {
        showNotification(`Test failed: ${error.message}`, 'error');
    }
}

// Test endpoints population
async function populateTestEndpoints(summary) {
    const testEndpoint = document.getElementById('test-endpoint');
    
    try {
        // Try to get real mappings from WireMock server
        const response = await fetch('http://localhost:8080/__admin/mappings');
        
        if (response.ok) {
            const data = await response.json();
            const mappings = data.mappings || [];
            
            if (mappings.length > 0) {
                
                // Group mappings by API for organized dropdown
                const groupedMappings = groupMappingsBySpec(mappings);
                
                let optionsHTML = '<option value="">Select an endpoint...</option>';
                
                Object.entries(groupedMappings).forEach(([apiName, apiMappings]) => {
                    optionsHTML += `<optgroup label="${apiName} (${apiMappings.length} endpoints)">`;
                    
                    // Get unique endpoints to avoid duplicates
                    const uniqueEndpoints = [...new Map(apiMappings.map(mapping => {
                        const method = mapping.request.method || 'GET';
                        const url = mapping.request.url || mapping.request.urlPattern || '/';
                        return [`${method}_${url}`, { method, url }];
                    })).values()];
                    
                    uniqueEndpoints.slice(0, 8).forEach(endpoint => {
                        // Don't URL encode the endpoint.url since it might contain patterns like {id}
                        const displayUrl = endpoint.url.replace(/\{([^}]+)\}/g, '${$1}'); // Show patterns clearly
                        optionsHTML += `<option value="${endpoint.url}" data-method="${endpoint.method}" data-api="${apiName}">
                            ${endpoint.method} ${displayUrl}
                        </option>`;
                    });
                    
                    optionsHTML += '</optgroup>';
                });
                
                testEndpoint.innerHTML = optionsHTML;
                return;
            }
        }
    } catch (error) {
        console.warn('⚠️ Could not fetch real mappings for test endpoints, using mock data:', error);
    }
    
    // Fallback to mock data
    const mappings = generateMockMappings(summary);
    
    // Group options by API
    const groupedOptions = groupMappingsByAPI(mappings);
    
    let optionsHTML = '<option value="">Select an endpoint...</option>';
    
    Object.keys(groupedOptions).forEach(apiName => {
        optionsHTML += `<optgroup label="${apiName}">`;
        
        // Get unique endpoints for this API (avoid duplicates from different scenarios)
        const uniqueEndpoints = [...new Map(groupedOptions[apiName].map(mapping => 
            [`${mapping.method}_${mapping.path}`, mapping]
        )).values()];
        
        uniqueEndpoints.slice(0, 8).forEach(mapping => {
            optionsHTML += `<option value="${mapping.path}" data-method="${mapping.method}" data-api="${apiName}">
                ${mapping.method} ${mapping.path}
            </option>`;
        });
        
        optionsHTML += '</optgroup>';
    });
    
    testEndpoint.innerHTML = optionsHTML;
}

function showAllMappings(apiName) {
    const mappings = window.allMappings || [];
    const apiMappings = mappings.filter(m => m.apiName === apiName);
    
    // Show all mappings in a new modal or expand the current view
    showNotification(`Found ${apiMappings.length} mappings for ${apiName}`, 'info');
    
    // You could implement a detailed view here
}

// Live testing functionality
async function executeTest() {
    const baseUrl = document.getElementById('test-base-url').value;
    const endpoint = document.getElementById('test-endpoint').value;
    const scenario = document.getElementById('test-scenario').value;
    const method = document.getElementById('test-endpoint').selectedOptions[0]?.dataset.method || 'GET';
    
    if (!endpoint) {
        showNotification('Please select an endpoint to test', 'error');
        return;
    }
    
    const resultsDiv = document.getElementById('test-results');
    
    // Replace URL patterns with sample values for testing
    let testUrl = endpoint;
    if (testUrl.includes('{id}')) {
        testUrl = testUrl.replace('{id}', '123');
    }
    if (testUrl.includes('{userId}')) {
        testUrl = testUrl.replace('{userId}', 'user123');
    }
    if (testUrl.includes('{accountId}')) {
        testUrl = testUrl.replace('{accountId}', 'acc123');
    }
    // Add more pattern replacements as needed
    testUrl = testUrl.replace(/\{([^}]+)\}/g, 'sample-$1');
    
    const fullUrl = `${baseUrl}${testUrl}`;
    
    // Show loading
    resultsDiv.innerHTML = '<div class="text-blue-600"><i class="fas fa-spinner fa-spin mr-2"></i>Executing test...</div>';
    
    try {
        // Create test payload
        const testPayload = {
            [scenario]: true,
            test_data: `Testing ${scenario} scenario`,
            timestamp: new Date().toISOString()
        };
        
        const requestOptions = {
            method,
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        };
        
        if (method !== 'GET') {
            requestOptions.body = JSON.stringify(testPayload);
        }
        
        const startTime = Date.now();
        const response = await fetch(fullUrl, requestOptions);
        const endTime = Date.now();
        const responseText = await response.text();
        
        let responseData;
        try {
            responseData = JSON.parse(responseText);
        } catch {
            responseData = responseText;
        }
        
        // Display results
        resultsDiv.innerHTML = `
            <div class="space-y-3">
                <div class="flex items-center justify-between">
                    <span class="font-medium">Test Results</span>
                    <span class="text-xs text-gray-500">${endTime - startTime}ms</span>
                </div>
                <div class="grid grid-cols-2 gap-4 text-xs">
                    <div>
                        <div class="font-medium text-gray-700">Request</div>
                        <div class="bg-gray-100 p-2 rounded mt-1">
                            <div><strong>Method:</strong> ${method}</div>
                            <div><strong>Pattern:</strong> ${endpoint}</div>
                            <div><strong>Test URL:</strong> ${fullUrl}</div>
                            <div><strong>Scenario:</strong> ${scenario}</div>
                        </div>
                    </div>
                    <div>
                        <div class="font-medium text-gray-700">Response</div>
                        <div class="bg-gray-100 p-2 rounded mt-1">
                            <div><strong>Status:</strong> <span class="${response.ok ? 'text-green-600' : 'text-red-600'}">${response.status}</span></div>
                            <div><strong>Content-Type:</strong> ${response.headers.get('content-type') || 'N/A'}</div>
                        </div>
                    </div>
                </div>
                <div>
                    <div class="font-medium text-gray-700 mb-1">Response Body</div>
                    <div class="bg-gray-100 p-2 rounded text-xs overflow-auto max-h-32">
                        <pre>${typeof responseData === 'object' ? JSON.stringify(responseData, null, 2) : responseData}</pre>
                    </div>
                </div>
            </div>
        `;
        
    } catch (error) {
        resultsDiv.innerHTML = `
            <div class="text-red-600">
                <div class="font-medium mb-2">Test Failed</div>
                <div class="text-sm bg-red-50 p-3 rounded">
                    <strong>Error:</strong> ${error.message}<br>
                    <strong>Pattern:</strong> ${endpoint}<br>
                    <strong>Test URL:</strong> ${fullUrl}<br>
                    <strong>Method:</strong> ${method}
                </div>
            </div>
        `;
    }
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 z-50 p-4 rounded-md shadow-lg ${getNotificationColor(type)} transform transition-all duration-300`;
    notification.innerHTML = `
        <div class="flex items-center">
            <i class="fas ${getNotificationIcon(type)} mr-2"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function getNotificationColor(type) {
    const colors = {
        'success': 'bg-green-100 border border-green-400 text-green-700',
        'error': 'bg-red-100 border border-red-400 text-red-700',
        'warning': 'bg-yellow-100 border border-yellow-400 text-yellow-700',
        'info': 'bg-blue-100 border border-blue-400 text-blue-700'
    };
    return colors[type] || colors.info;
}

function getNotificationIcon(type) {
    const icons = {
        'success': 'fa-check-circle',
        'error': 'fa-times-circle',
        'warning': 'fa-exclamation-triangle',
        'info': 'fa-info-circle'
    };
    return icons[type] || icons.info;
}
