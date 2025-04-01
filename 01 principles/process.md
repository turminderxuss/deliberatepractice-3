# Vibe Coding Process

## Overview

This document outlines the process for developing software using the "Vibe Coding" methodology, which leverages LLM agents (particularly Claude) to handle the entire software development process with minimal manual coding. The focus is on rapid iteration, feedback loops, and test-driven development.

## Core Process Phases

### 1. Specifications Process

The specifications process transforms high-level intent into formal, actionable specifications:

1. **Requirements Gathering**
   - Use Claude to interview stakeholders and gather requirements
   - Generate user stories and acceptance criteria with Claude
   - Capture vague "vibes" and transform them into concrete specifications

2. **Specification Formalization**
   - Format specifications in structured Markdown files
   - Use Gherkin syntax (Given/When/Then) for behavior-driven specifications
   - Define formal contracts with preconditions, postconditions, and invariants

3. **Architecture Design**
   - Generate system diagrams as PlantUML code
   - Use VS Code PlantUML viewer for visualization
   - Iterate on diagrams through screenshot-based feedback
   - Document architecture decisions in ADR format

### 2. Fully Automated Coding

The coding process follows a strict test-driven approach:

1. **Test-Driven Development**
   - Generate test cases first based on specifications
   - Write tests that validate formal contracts
   - Implement property-based tests for thorough validation

2. **Implementation**
   - Generate implementation code to pass existing tests
   - Ensure code adheres to architectural boundaries
   - Follow design-by-contract principles

3. **Code Review & Refinement**
   - Implement layered AI review process
   - One LLM generates implementation, another reviews it
   - Integrate static analysis tools
   - Refine code based on review feedback

4. **Documentation Generation**
   - Auto-generate docstrings, README files, and API docs
   - Ensure documentation aligns with implementation

### 3. Automated Testing & External Review

Comprehensive testing ensures quality:

1. **Unit Testing**
   - Execute tests created during TDD phase
   - Analyze test failures and implement fixes

2. **Integration Testing**
   - Test interactions between components
   - Verify end-to-end functionality

3. **Property-Based Testing & Fuzzing**
   - Generate thousands of test cases
   - Actively try to break the implementation
   - Detect and eliminate non-deterministic behavior

4. **External Validation**
   - Package code for external review
   - Integrate with code quality tools

### 4. CI/CD Pipeline & Monitoring

Continuous delivery and feedback:

1. **Continuous Integration**
   - GitHub Actions for automated testing
   - Pre-commit hooks for code formatting and linting

2. **Deployment Automation**
   - Automated deployment to target environments
   - Containerization for consistent environments

3. **Observability & Monitoring**
   - Comprehensive logging, monitoring, and tracing
   - Anomaly detection for non-deterministic behaviors
   - System self-documentation through behavior recording

4. **Feedback Loop**
   - Feed monitoring data back to LLM for improvement
   - Continuous refinement based on production behavior

## Iterative Development Cycle

The Vibe Coding process is inherently iterative:

1. **Start with MVP**: Focus on a minimal viable product
2. **Rapid Iteration**: Build, test, review, and refine in short cycles
3. **Incremental Expansion**: Add functionality incrementally
4. **Continuous Feedback**: Use real-world feedback to guide development

## Best Practices

- **Clear Intent Communication**: Clearly communicate intent to Claude
- **Atomic Development**: Build one component at a time
- **Comprehensive Testing**: Test thoroughly at each step
- **Documentation First**: Keep documentation aligned with code
- **Feedback Integration**: Continuously integrate feedback

By following this process, you can rapidly develop high-quality software with minimal manual coding, leveraging Claude to handle implementation details while you focus on high-level direction and architecture.