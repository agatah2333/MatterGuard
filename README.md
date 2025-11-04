# MatterGuard: Automated Testing Framework for Matter Protocol

# Note: [![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC_BY--NC_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

## Quick Start (Pre-compiled Executables)

**MatterGuard provides standalone executables that run without Python installation.**

This distribution includes pre-compiled tools for Ubuntu 22.04+ that enable automated testing of Matter protocol implementations.

---

## Table of Contents

- [System Requirements](#system-requirements)
- [Quick Installation](#quick-installation)
- [Available Tools](#available-tools)
- [Environment Setup](#environment-setup)
- [Usage Guide](#usage-guide)
  - [Tool 1: Convert XML Data Format](#tool-1-convert-xml-data-format)
  - [Tool 2: Create OpenAI Assistant](#tool-2-create-openai-assistant)
  - [Tool 3: Generate Test Cases](#tool-3-generate-test-cases)
  - [Tool 4: Static Analysis](#tool-4-static-analysis)
  - [Tool 5: Dynamic Testing](#tool-5-dynamic-testing)
- [Data Files](#data-files)
- [Troubleshooting](#troubleshooting)
- [For Developers](#for-developers)

---

## System Requirements

### Hardware and Operating System

- **Operating System**: Ubuntu 22.04 LTS or newer (x86-64 architecture)
- **Python**: **NOT REQUIRED** - executables are standalone
- **Disk Space**: ~500 MB for executables and data files

### Prerequisites

- OpenAI API key for LLM-based test generation
- Matter specification files (available from [CSA-IOT](https://csa-iot.org/developer-resource/specifications-download-request/))
- chip-tool binary for dynamic testing (from Matter SDK)
- Virtual Matter device applications for testing

---


### Verify Installation

Test that executables work:

```bash
./convert_xml_to_small/convert_xml_to_small --help
```

You should see the help output.

---

## Available Tools

MatterGuard provides 5 standalone executables:

| Tool | Purpose | Size |
|------|---------|------|
| **convert_xml_to_small** | Convert XML cluster data to simplified JSON format | 19 MB |
| **create_assistant** | Create OpenAI Assistant with Matter specifications | 31 MB |
| **llmprompt** | Generate LLM-based test cases for clusters | 31 MB |
| **static_analysis** | Validate cluster specifications against XML ground truth | 19 MB |
| **run_dynamic_tests** | Execute dynamic tests against live Matter devices | 22 MB |

All executables are located in their respective directories with dependencies bundled.

---

## Environment Setup

### 1. Configure OpenAI API Key

Create the environment configuration file:

```bash
cp .env.example .env
```

Edit the `.env` file and add your OpenAI API key:

```bash
OPENAI_API_KEY=your-actual-api-key-here
```

### 2. Prepare Matter SDK Components

For dynamic testing, you'll need:

**chip-tool (Matter Controller)**
- Command-line Matter controller used to commission and interact with Matter devices
- A single chip-tool build can be reused across different Matter versions for testing

**Virtual Device Applications**
- Virtual Matter devices simulate real IoT devices for testing purposes
- `chip-all-clusters-app`: Comprehensive virtual device implementing most Matter clusters

**Note**: Compilation instructions follow the official Matter SDK build process. Refer to the [Matter SDK documentation](https://github.com/project-chip/connectedhomeip) for version-specific build requirements.

### 3. Start and Pair Matter Device

#### 3.1. Start Virtual Device Application

```bash
cd /path/to/connectedhomeip
./out/debug/chip-all-clusters-app
```

**Important**: The application will display a manual pairing code. Look for:

```
Manual pairing code: [MT:-24J0AFN00KA0648G00]
```

Save this code - you'll need it for commissioning.

#### 3.2. Commission Device with chip-tool

In a new terminal:

```bash
cd /path/to/connectedhomeip
./out/debug/standalone/chip-tool pairing code 0x654324 MT:-24J0AFN00KA0648G00
```

**Parameters**:
- `0x654324`: Node ID assigned to the device (hexadecimal format)
- `MT:-24J0AFN00KA0648G00`: Manual pairing code from device application

#### 3.3. Verify Pairing

Test the connection:

```bash
./out/debug/standalone/chip-tool basicinformation read vendor-name 0x654324 0
```

Expected: The command should return the device's vendor name without errors.

**Note on Pairing Persistence**:
- Pairing credentials are stored in `/tmp/chip_*` directories
- Credentials are **volatile** and will be **lost on system reboot**
- After system restart, you must re-run the pairing procedure
- Use the same node ID (`0x654324` by default) for consistency

---

## Usage Guide

### Tool 1: Convert XML Data Format

Convert complete XML cluster definitions to simplified JSON format for test generation.

**Location**: `convert_xml_to_small/convert_xml_to_small`

#### Basic Usage

```bash
# Extract all clusters
./convert_xml_to_small/convert_xml_to_small \
    --input Static/v1.4/xml_data.json \
    --output small.json \
    --all

# Extract specific clusters
./convert_xml_to_small/convert_xml_to_small \
    --input Static/v1.4/xml_data.json \
    --output small.json \
    --clusters "scenes,onoff,doorlock"
```

#### Input/Output

- **Input**: `Static/v1.x/xml_data.json` (extracted cluster definitions)
- **Output**: `small.json` (simplified format for llmprompt tool)

---

### Tool 2: Create OpenAI Assistant

Create an OpenAI Assistant configured with Matter specification documents.

**Location**: `create_assistant/create_assistant`

#### Setup (First Time Only)

```bash
# Ensure .env file exists with your OpenAI API key
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=your-key-here

# Create assistant with specification files
./create_assistant/create_assistant -p /path/to/matter/spec/files
```

This uploads specification files to OpenAI's vector store and automatically saves `ASSISTANT_ID` and `VECTOR_STORE_ID` to your `.env` file.

#### Output

The tool updates your `.env` file with:
```
ASSISTANT_ID=asst_xxxxx
VECTOR_STORE_ID=vs_xxxxx
```

---

### Tool 3: Generate Test Cases

Generate LLM-based test cases for Matter clusters using the configured Assistant.

**Location**: `llmprompt/llmprompt`

#### Prerequisites

1. `.env` file with `OPENAI_API_KEY`, `ASSISTANT_ID`, `VECTOR_STORE_ID`
2. `small.json` file in the current directory (from Tool 1)

#### Usage

```bash
# Copy small.json to llmprompt directory (or run from project root)
cp small.json llmprompt/
cd llmprompt

# Generate test cases
./llmprompt
```

#### Output Structure

- `clusters_batch_results/` - Batch query results for cluster discovery
- `testcases/<ClusterName>/` - Generated test cases organized by cluster
  - `command_{id}.txt` - Command test cases
  - `attribute_{id}.txt` - Attribute test cases
  - `event_{id}.txt` - Event test cases

**Note**: Execution time ranges from several minutes to tens of minutes depending on API rate limits.

---

### Tool 4: Static Analysis

Validate LLM-generated cluster specifications against XML ground truth.

**Location**: `static_analysis/static_analysis`

#### Usage

The static analysis tool must be run from within a version directory that contains the required data files.

```bash
# Copy executable to version directory
cp static_analysis/static_analysis Static/v1.0/

# Navigate to version directory
cd Static/v1.0

# Run analysis
./static_analysis
```

#### Required Files in Working Directory

- `xml_data.json` - Ground truth cluster definitions from XML
- `extracted/` - Directory containing LLM-extracted JSON cluster data

#### Output Files

| File | Description |
|------|-------------|
| `comprehensive_comparison_results.json` | Detailed comparison of all cluster specifications |
| `validation_tests.json` | Generated boundary-value test cases |

#### Console Output

The analysis provides a summary report including:
- Total clusters analyzed
- Number of discrepancies found
- Categories of validation errors
- Overall conformance percentage

---

### Tool 5: Dynamic Testing

Execute generated test cases against running Matter devices.

**Location**: `run_dynamic_tests/run_dynamic_tests`

#### Prerequisites

1. chip-tool binary from Matter SDK
2. Running and paired Matter device (see [Environment Setup](#environment-setup))
3. YAML test files in `Dynamic/v1.x/yamltests/`
4. Extracted cluster specifications in `Static/v1.x/extracted/`

#### Usage Examples

**Run all tests for a version:**

```bash
./run_dynamic_tests/run_dynamic_tests \
    --chip-tool /path/to/chip-tool \
    --path Dynamic/v1.0/yamltests \
    --extracted-dir Static/v1.0/extracted \
    --all
```

**Run tests for specific cluster:**

```bash
./run_dynamic_tests/run_dynamic_tests \
    --chip-tool /path/to/chip-tool \
    --path Dynamic/v1.4/yamltests \
    --extracted-dir Static/v1.4/extracted \
    --cluster level-control
```

**Run single test file:**

```bash
./run_dynamic_tests/run_dynamic_tests \
    --chip-tool /path/to/chip-tool \
    --file Dynamic/v1.0/yamltests/0x0008-level-control-cluster/Test_TC_LVL_1_1.yaml \
    --extracted-dir Static/v1.0/extracted
```

**Custom device configuration:**

```bash
./run_dynamic_tests/run_dynamic_tests \
    --chip-tool /path/to/chip-tool \
    --path Dynamic/v1.0/yamltests \
    --extracted-dir Static/v1.0/extracted \
    --node-id 0x123456 \
    --endpoint 2 \
    --all
```

#### Output Structure

Test results are saved to the specified output directory (`test_results` by default):

```
test_results/
├── summary.json           # Overall test execution summary
├── passed/                # Logs from passed tests
├── failed/                # Logs from failed tests
└── errors/                # Error traces and diagnostics
```

---

## Data Files

The distribution includes essential data files:

### Static Directory (`Static/`)

Contains cluster specifications and analysis data for different Matter versions:

```
Static/
├── v1.0/
│   ├── xml_data.json         # Ground truth cluster definitions
│   └── extracted/            # LLM-generated cluster specs
├── v1.1/
│   ├── xml_data.json
│   └── extracted/
├── v1.2/
│   ├── xml_data.json
│   └── extracted/
├── v1.3/
│   ├── xml_data.json
│   └── extracted/
└── v1.4/
    ├── xml_data.json
    └── extracted/
```

### Dynamic Directory (`Dynamic/`)

Contains YAML test files for dynamic testing:

```
Dynamic/
├── v1.0/
│   └── yamltests/           # v1.0 YAML test files
├── v1.1/
│   └── yamltests/           # v1.1 YAML test files
├── v1.2/
│   └── yamltests/           # v1.2 YAML test files
├── v1.3/
│   └── yamltests/           # v1.3 YAML test files
└── v1.4/
    └── yamltests/           # v1.4 YAML test files
```

---

## Troubleshooting

### Executable Won't Run

```bash
# Check if executable
ls -l convert_xml_to_small/convert_xml_to_small

# Make executable if needed
chmod +x convert_xml_to_small/convert_xml_to_small
```

### Data Files Not Found

**Error**: Tools can't find `xml_data.json` or other data files

**Solution**: Run executables from the correct working directory or provide full paths:

```bash
# Good - run from directory with data files
cd /path/to/matterguard_executables
./static_analysis/static_analysis

# Or copy data to executable location
cp -r Static/ /path/to/executables/
```

### OpenAI API Errors

**Error**: `OPENAI_API_KEY not found in .env file`

**Solution**: Ensure `.env` file exists in the working directory:

```bash
# Copy .env to working directory
cp .env /my/working/directory/

# Or set environment variables
export OPENAI_API_KEY="your-key-here"
export ASSISTANT_ID="asst_xxxxx"
export VECTOR_STORE_ID="vs_xxxxx"
```

### chip-tool Not Found

**Error**: Dynamic tests can't find chip-tool

**Solution**: Provide full path to chip-tool:

```bash
./run_dynamic_tests/run_dynamic_tests \
    --chip-tool /full/path/to/connectedhomeip/out/debug/standalone/chip-tool \
    --path Dynamic/v1.0/yamltests \
    --extracted-dir Static/v1.0/extracted \
    --all
```


### Pairing Credentials Lost After Reboot

**Issue**: Device pairing fails after system restart

**Solution**: Pairing credentials in `/tmp/chip_*` are volatile. Re-run the pairing procedure:

```bash
./out/debug/standalone/chip-tool pairing code 0x654324 MT:-24J0AFN00KA0648G00
```

---

## Workflow Summary

Here's the complete testing workflow using the pre-compiled executables:

### 1. Initial Setup (One Time)

# Configure OpenAI
cp .env.example .env
# Edit .env with your API key

# Create OpenAI Assistant
./create_assistant/create_assistant -p /path/to/matter/specs/
```

### 2. Prepare Test Configuration

```bash
# Convert XML to test configuration
./convert_xml_to_small/convert_xml_to_small \
    --input Static/v1.4/xml_data.json \
    --output small.json \
    --clusters "scenes,onoff,levelcontrol"
```

### 3. Generate Test Cases

```bash
# Generate LLM-based test cases
./llmprompt/llmprompt
```

### 4. Static Validation

```bash
# Validate cluster specifications
cd Static/v1.4
../../static_analysis/static_analysis
cd ../..
```

### 5. Dynamic Testing

```bash
# Setup Matter device (see Environment Setup)
# Then run tests:
./run_dynamic_tests/run_dynamic_tests \
    --chip-tool /path/to/chip-tool \
    --path Dynamic/v1.4/yamltests \
    --extracted-dir Static/v1.4/extracted \
    --all
```

## Additional Resources

### Matter Protocol Resources

- [Matter Specification](https://csa-iot.org/developer-resource/specifications-download-request/)
- [Matter SDK (connectedhomeip)](https://github.com/project-chip/connectedhomeip)
- [ZAP Tool Documentation](https://github.com/project-chip/zap)

### OpenAI Resources

- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [Assistants API Guide](https://platform.openai.com/docs/assistants/overview)
